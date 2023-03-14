# This handles the advance endpoint logic


from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.exceptions import NotFound 

from core.models import Advance, ScheduledPayment
from .serializers import (AdvanceSerializer, 
AdvanceDetailSerializer, 
AdvanceListSerializer,
ScheduledPaymentSerializer,)

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

import math

import datetime

import pandas as pd

# These are loan terms and rates used for backend calculations
# This is done so that the client won't be able to game the calcs
terms_and_rates = [[3, 0.2299, 0.1289], [6, 0.2299, 0.1289],
    [12, 0.2299, 0.1289], [24, 0.2099, 0.1166],
    [36, 0.1899, 0.1065], [48, 0.1699, 0.0962], 
    [60, 0.1499, 0.0854]
]

class AdvanceListView(APIView):
    serializer_class = AdvanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # This creates the advance
    def post(self, request):
        advance_to_create = AdvanceSerializer(data=request.data)
        try:
            advance_to_create.is_valid(raise_exception=True)
            advance_to_create.save(user_id=request.user.id)
            return Response(advance_to_create.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AllAdvanceListView(APIView):
    serializer_class = AdvanceListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # This fetches the advance list for the user dashboard
    def get(self, request):
        advances = Advance.objects.filter(user_id=request.user.id).order_by("created_on")
        # print("advances ->", advances)
        serialized_advances = AdvanceListSerializer(advances, many=True)
        # print(serialized_advances)
        return Response(serialized_advances.data, status=status.HTTP_200_OK)


class AdvanceDetailedView(APIView):
    serializer_class = AdvanceDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # This checks if the requested advance exists
    def get_advance(self, pk):
        try:
            return Advance.objects.get(pk=pk)
        except Advance.DoesNotExist:
            raise NotFound(detail="Advance not found")

    # This fetches the requested advance details
    def get(self, request, pk):
        advance = self.get_advance(pk=pk)
        serialized_advance = AdvanceDetailSerializer(advance)
        return Response(serialized_advance.data)
    
    # When the advance is in "Incomplete" state, then the user 
    # is allowed to delete it 
    # Else, the user cannot delete that advance
    def delete(self, request, pk):
        advance_to_delete = self.get_advance(pk=pk)
        
        if advance_to_delete.status != "Incomplete":
            return Response({"message": "Action not allowed"}, 
            status=status.HTTP_401_UNAUTHORIZED)

        advance_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # This allows the user to edit the advance details when 
    # the advance is in "Incomplete" state
    def patch(self, request, pk):
        # print(request)
        # print(request.FILES)

        advance_to_update = self.get_advance(pk=pk)

        # print(advance_to_update.status)

        # We let the user edit advance details when the advance
        # is in "Incomplete" state
        if advance_to_update.status != "Incomplete":
            return Response({"message": "Action not allowed"}, 
            status=status.HTTP_401_UNAUTHORIZED)

        updated_advance = AdvanceDetailSerializer(advance_to_update, data=request.data, partial=True)
        # print(advance_to_update.status)
        try:
            updated_advance.is_valid(raise_exception=True)
            updated_advance.save()
            # print(advance_to_update.status)
            # The below if block calculates and sets the advance
            # interest rate, term and total amount payable
            if "loan_amount" in request.data and "loan_term" in request.data:
                # print("if statement triggered")
                for rate in terms_and_rates:
                    # print("for loop started")
                    if request.data["loan_term"] == rate[0]:
                        # print("if statement inside loop triggered")
                        advance_to_update.loan_interest_rate = rate[1]
                        advance_to_update.annualised_fee = rate[2]
                        advance_to_update.save()
                term = advance_to_update.loan_term
                interest_rate = advance_to_update.loan_interest_rate
                amount = float(advance_to_update.loan_amount)
                # print(type(amount))
                interest_rate_monthly = float(interest_rate / 12)
                # print(type(interest_rate_monthly))
                x = math.pow(1 + interest_rate_monthly, term)
                # print(type(x))
                advance_to_update.estimated_loan_monthly_payment = ((
                    amount * x * interest_rate_monthly
                ) / (x - 1))
                advance_to_update.save()
                # print(advance_to_update.status)
            # The below if block checks if the user is submitting the advance or not
            # If they are submitting, then the advance status changes to
            # "Pending approval"
            # This triggers the for loop that generates a list of payments
            # that the user will see on the frontend
            if "is_submitting_loan" in request.data and request.data["is_submitting_loan"] == True:
                # print(advance_to_update.status)
                advance_to_update.status = "Pending approval"
                advance_to_update.save()
                # print(advance_to_update.loan_term)
                current_date = datetime.date.today().replace(day=1)
                for term in range(1, advance_to_update.loan_term + 1):
                    # print(term)
                    ScheduledPayment.objects.create(
                        user=advance_to_update.user,
                        advance_id=advance_to_update.id,
                        amount=advance_to_update.estimated_loan_monthly_payment,
                        due_date=pd.to_datetime(current_date) + pd.DateOffset(months=term)
                    )
                # print(advance_to_update.status)
            return Response(updated_advance.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ScheduledPaymentView(APIView):
    serializer_class = ScheduledPaymentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    # This provides the schedule of all payments for the requested advance
    def get(self, request, pk):
        # print("request data", request)
        payments = ScheduledPayment.objects.filter(advance_id=pk).order_by("due_date")
        # print("advances ->", advances)
        serialized_advances = ScheduledPaymentSerializer(payments, many=True)
        # print(serialized_advances)
        return Response(serialized_advances.data, status=status.HTTP_200_OK)


