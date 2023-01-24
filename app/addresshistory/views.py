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

    def patch(self, request, pk):
        address_to_update = self.get_address(pk)
        if address_to_update.user != request.user:
            raise PermissionDenied("Unauthorised")
        old_address_duration = address_to_update.duration
        print(old_address_duration)
        new_address_duration = request.data["duration"]
        print(new_address_duration)
        duration_difference = new_address_duration - old_address_duration
        updated_address = AddressHistorySerializer(address_to_update, data=request.data)
        print(duration_difference)
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


