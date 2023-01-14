import uuid
from shortuuid.django_fields import ShortUUIDField

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255, default="")

    is_identity_verified = models.BooleanField(default=False)
    has_address_history = models.BooleanField(default=False)
    total_address_duration = models.PositiveIntegerField(default=0)

    username = None


    objects = UserManager()

    USERNAME_FIELD = "email"


class Advance(models.Model):
    """Advance object"""
    id = ShortUUIDField(
        primary_key=True,
        length=8,
        alphabet="ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    description = models.TextField(max_length=1000)
    reason = models.TextField(max_length=100, default="")
    first_line_address = models.CharField(max_length=255)
    second_line_address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    town_or_city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    lease_agreement_file = models.FileField()
    rent_protection_policy_file = models.FileField()
    tenant_vetting_file = models.FileField()
    amount_of_rent_selling = models.DecimalField(max_digits=8, decimal_places=2)

    estimated_monthly_payment = models.DecimalField(max_digits=8, decimal_places=2)
    
    name_on_bank_account = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=100)
    sort_code_bank_account = models.CharField(max_length=100)

    admin_comment = models.TextField(max_length=1000, default="")


class AddressHistory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    first_line_address = models.CharField(max_length=255)
    second_line_address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    town_or_city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()

