"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from core.models import PasswordResetToken
from core.models import User

from rest_framework.views import APIView

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import APIException

import random
import string

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


class ForgotPasswordView(APIView):

    def post(self, request):

        token = "".join(random.choice(string.ascii_uppercase + string.digits) 
            for _ in range(100))
        
        PasswordResetToken.objects.create(
            email=request.data["email"],
            token=token
        )

        user = User.objects.filter(email=request.data["email"])

        if not user:
            raise APIException("Invalid email address")

        url = "http://localhost:3000/password-reset/" + token

        send_mail('Reset your Factored password',
        'Please click on the below link to reset your Factored password. %s' % url,
        'notifications@factored.co',
        [request.data["email"],],
        fail_silently=False)

        return Response(status=status.HTTP_201_CREATED)


class ResetPasswordView(APIView):
    def post(self, request):
        # print(request.data)
        reset_password = PasswordResetToken.objects.filter(token=request.data["token"]).first()

        if not reset_password:
            raise APIException("Password reset link invalid")

        user = User.objects.filter(email=reset_password.email).first()

        if not user:
            raise APIException("Invalid credentials")

        user.set_password(request.data["password"])
        user.save()

        return Response(status=status.HTTP_200_OK)

