"""
Views for the address history API
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import AddressHistory
from addresshistory import serializers

class AddressHistoryViewset(viewsets.ModelViewSet):
    serializer_class = serializers.AddressHistorySerializer
    queryset = AddressHistory.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        # return super().destroy(request, *args, **kwargs)

    # def get_serializer_class(self):
    #     return self.serializer_class




