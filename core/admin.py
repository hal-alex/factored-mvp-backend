"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
from .models import AddressHistory, Advance, ScheduledPayment


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 
    'mobile_number', 'is_identity_verified', 'is_address_verified', 'has_address_history']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'id')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name',
            'mobile_number','is_identity_verified', 'is_address_verified', 'has_address_history' )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login', 'id']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
# admin.site.register(models.Advance)


@admin.register(Advance)
class AdvanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_on', 'status', 
    'postcode', 'monthly_rent', 'loan_amount', 'loan_interest_rate', 
    'estimated_loan_monthly_payment',]
    

# admin.site.register(models.AddressHistory)

@admin.register(AddressHistory)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_line_address', 'second_line_address',
    'postcode', 'country', 'start_date', 'end_date', 'duration']


@admin.register(ScheduledPayment)
class ScheduledPaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "advance", "status", "amount", "due_date"]
    ordering = ("due_date",)

