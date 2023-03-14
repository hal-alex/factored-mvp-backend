# This handles the address history endpoint logic
# Before a user can create an advance, they have to provide address history for
# 36 months or more

# The frontend allows the user to create a single address, then specify the
# starting and ending date, and provides the total duration at that address


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from core.models import AddressHistory, User
from user.serializers import UserSerializer

from .serializers import AddressHistorySerializer


from rest_framework.authentication import TokenAuthentication


class AddressHistoryListView(APIView):
    serializer_class = AddressHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # This adds the address to the database
    # It also checks if total_address_duration is over 36 months
    # If true, then has_address_history is flagged as true
    # This means that we have enough address info to pass this check
    def post(self, request):
        # print(request.data)
        address_to_create = AddressHistorySerializer(data=request.data) 
        try:
            address_to_create.is_valid()
            address_to_create.save(user_id=request.user.id)
            requested_user = User.objects.get(id=request.user.id) 
            requested_user.total_address_duration += request.data["duration"]
            requested_user.save()
            if requested_user.total_address_duration >= 36:
                    requested_user.has_address_history = True
                    requested_user.save()
            return Response(address_to_create.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    # This fetches the address history belonging to the user
    def get(self, request):
        addresses = AddressHistory.objects.filter(user_id=request.user.id)
        serialized_addresses = AddressHistorySerializer(addresses, many=True)
        return Response(serialized_addresses.data, status=status.HTTP_200_OK)



class AddressHistoryDetailView(APIView):
    serializer_class = AddressHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # This checks if an address history exists
    def get_address(self, pk):
        try:
            return AddressHistory.objects.get(pk=pk)
        except AddressHistory.DoesNotExist:
            raise NotFound("Address not found!")

    # This handles the logic for when the user edits an existing address
    def patch(self, request, pk):
        address_to_update = self.get_address(pk)
        # We check if the address history belongs to the user
        if address_to_update.user != request.user:
            raise PermissionDenied("Unauthorised")
        old_address_duration = address_to_update.duration
        print(old_address_duration)
        new_address_duration = request.data["duration"]
        print(new_address_duration)
        # We calculate the difference between the old duration and new duration
        duration_difference = new_address_duration - old_address_duration
        updated_address = AddressHistorySerializer(address_to_update, data=request.data)
        print(duration_difference)
        # This block deals with total_address_duration and has_address_history logic
        # total_address_duration is a running total that changes when 
        # a new address is added or when an existing address is changed
        # has_address_history is a boolean flag that changes when 
        # total_address_duration is over 36
        try:
            updated_address.is_valid(raise_exception=True)
            updated_address.save()
            if duration_difference != 0:
                requested_user = User.objects.get(id=request.user.id) 
                requested_user.total_address_duration += duration_difference
                requested_user.save()
                if requested_user.total_address_duration >= 36:
                    requested_user.has_address_history = True
                    requested_user.save()
                elif requested_user.total_address_duration < 36:
                    requested_user.has_address_history = False
                    requested_user.save() 
            return Response(updated_address.data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # This deletes an address belonging to a user
    # As all addresses have a duration e.g. how many months the used lived there
    # When a user deletes an address, we reduce the amount of months
    # of address history we have on file
    # Otherwise, the total_address_duration would not be affected
    # whenever the user would delete an address
    def delete(self, request, pk):
        address_to_delete = self.get_address(pk)
        if address_to_delete.user != request.user:
            raise PermissionDenied("Unauthorised")

        # print("duration", address_to_delete.duration)

        requested_user = User.objects.get(id=request.user.id) 
        requested_user.total_address_duration -= address_to_delete.duration
        requested_user.save()
        if requested_user.total_address_duration < 36:
            requested_user.has_address_history = False
            requested_user.save()
        
        address_to_delete.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)


