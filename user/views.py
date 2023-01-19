"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.views import APIView

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import status

class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage logged in user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Fetch and return the authenticated user"""
        return self.request.user


class SendEmailView(APIView):

    def get(self, request):
        send_mail('Alex testing Sendgrid integration', 
        'Reset your password.', 
        'notifications@factored.co', 
        ['info@factored.co',], 
        fail_silently=False)
        return Response(status=status.HTTP_202_ACCEPTED)

