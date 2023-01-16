
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.exceptions import NotFound 

from core.models import Advance
from .serializers import AdvanceSerializer, AdvanceDetailSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication


class AdvanceListView(APIView):
    serializer_class = AdvanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        advance_to_create = AdvanceSerializer(data=request.data)
        try:
            advance_to_create.is_valid(raise_exception=True)
            advance_to_create.save(user_id=request.user.id)
            return Response(advance_to_create.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def get(self, request):
        advances = Advance.objects.filter(user_id=request.user.id)
        # print("advances ->", advances)
        serialized_advances = AdvanceSerializer(advances, many=True)
        # print(serialized_advances)
        return Response(serialized_advances.data, status=status.HTTP_200_OK)


class AdvanceDetailedView(APIView):
    serializer_class = AdvanceDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_advance(self, pk):
        try:
            return Advance.objects.get(pk=pk)
        except Advance.DoesNotExist:
            raise NotFound(detail="Advance not found")


    def get(self, request, pk):
        advance = self.get_advance(pk=pk)
        serialized_advance = AdvanceDetailSerializer(advance)
        return Response(serialized_advance.data)
    
    def delete(self, request, pk):
        advance_to_delete = self.get_advance(pk=pk)
        advance_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        advance_to_update = self.get_advance(pk=pk)
        updated_advance = AdvanceSerializer(advance_to_update, data=request.data)

        try:
            updated_advance.is_valid(raise_exception=True)
            updated_advance.save()
            return Response(updated_advance.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    






# """
# Views for the advance API
# """

# from rest_framework import viewsets
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# from core.models import Advance
# from advance import serializers

# class AdvanceViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.AdvanceDetailSerializer
#     queryset = Advance.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

#     def get_serializer_class(self):
#         if self.action == "list":
#             return serializers.AdvanceSerializer
#         return self.serializer_class

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)



