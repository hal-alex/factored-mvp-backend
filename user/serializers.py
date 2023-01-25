from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    # def validate(self, data):
    #     title = data["title"]
    #     first_name = data["first_name"]
    #     last_name = data["last_name"]
    #     email = data["email"]
    #     password = data["password"]
    #     if title == "Please select":
    #         raise ValidationError({"title": "Select valid title"})
    #     elif not first_name.isalpha():
    #         raise ValidationError({"first_name": 
    #         "First name must be valid (only letters)"})
    #     elif not last_name.isalpha():
    #         raise ValidationError({"last_name": 
    #         "Last name must be valid (only letters)"})
    #     elif "@" not in email or "." not in email:
    #         raise ValidationError({"email": 
    #         "Email address must be valid"})
    #     elif len(password) < 8:
    #         raise ValidationError({"password": 
    #         "Password must be 8 chars long"})
    #     elif password == password.lower():
    #         raise ValidationError({"password": 
    #         "Password must contain at least one upper case letter"})
    #     elif not any(char.isdigit() for char in password):
    #         raise ValidationError({"password": 
    #         "Password must contain at least one number"})
        
    #     return data

    class Meta:
        model = get_user_model()
        fields = ["email",
        "title",
        "password",
        "first_name",
        "last_name",
        "mobile_number",
        "is_identity_verified",
        "has_address_history",
        "total_address_duration",
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return an updated user"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            raise ValidationError({"message": "Invalid credentials"})
        
        attrs["user"] = user
        return attrs
