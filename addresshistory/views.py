from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from core.models import AddressHistory
from .serializers import AddressHistorySerializer
from rest_framework.authentication import TokenAuthentication


class AddressHistoryListView(APIView):
    serializer_class = AddressHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # controller will allow us to post a review
    def post(self, request):
        print(request.data)
        address_to_create = AddressHistorySerializer(data=request.data) 
        try:
            address_to_create.is_valid()
            address_to_create.save(user_id=request.user.id)
            return Response(address_to_create.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
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

        return Response(status=status.HTTP_204_NO_CONTENT)


