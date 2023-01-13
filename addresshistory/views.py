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

    def post(self, request):
        # print(request.data)
        address_to_create = AddressHistorySerializer(data=request.data) 
        try:
            address_to_create.is_valid()
            address_to_create.save(user_id=request.user.id)
            # print(User.objects.get(id=request.user.id).has_address_history)
            all_addresses_belonging_to_user = AddressHistory.objects.filter(user_id=request.user.id)
            # print(all_addresses_belonging_to_user)
            total = 0
            for address in all_addresses_belonging_to_user:
                total += address.duration
                if total >= 36:
                    requested_user = User.objects.get(id=request.user.id) 
                    requested_user.has_address_history = True
                    requested_user.save()
            return Response(address_to_create.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e.__dict__ if e.__dict__ else str(e), 
            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def get(self, request):
        addresses = AddressHistory.objects.filter(user_id=request.user.id)
        serialized_addresses = AddressHistorySerializer(addresses, many=True)
        return Response(serialized_addresses.data, status=status.HTTP_200_OK)



class AddressHistoryDetailView(APIView):
    serializer_class = AddressHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_address(self, pk):
        try:
            return AddressHistory.objects.get(pk=pk)
        except AddressHistory.DoesNotExist:
            raise NotFound("Address not found!")

    def delete(self, request, pk):
        address_to_delete = self.get_address(pk)
        if address_to_delete.user != request.user:
            raise PermissionDenied("Unauthorised")

        address_to_delete.delete()

        all_addresses_belonging_to_user = AddressHistory.objects.filter(user_id=request.user.id)
            # print(all_addresses_belonging_to_user)
        total = 0
        for address in all_addresses_belonging_to_user:
            total += address.duration
            if total < 36:
                requested_user = User.objects.get(id=request.user.id) 
                requested_user.has_address_history = False
                requested_user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


