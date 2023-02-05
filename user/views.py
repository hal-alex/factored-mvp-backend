"""
Views for the user API.
"""
import json

import hmac

from rest_framework.views import csrf_exempt
from rest_framework.decorators import api_view

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

persona_whitelisted_addresses = ["35.232.44.140", "34.69.131.123", "34.67.4.225"] 

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

        url = "https://app.factored.co/password-reset/" + token

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




@api_view(['POST'])
@csrf_exempt
def webhook(request):
    persona_ip_address = request.META.get('HTTP_X_FORWARDED_FOR').split(",")[0]

    if persona_ip_address in persona_whitelisted_addresses: 
        jsonfied_data = json.loads(request.body.decode("utf-8"))

        if jsonfied_data["data"]["attributes"]["payload"]["data"]["attributes"]["status"] == "passed":
            user_id = jsonfied_data["data"]["attributes"]["payload"]["included"][0]["attributes"]["reference-id"]
            requested_user = User.objects.get(id=user_id)
            if not requested_user:
                pass
            else:
                requested_user.is_identity_verified = True
                requested_user.save()

    return Response(status=status.HTTP_200_OK)

