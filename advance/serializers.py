"""
Serializers for advance API
"""

from rest_framework import serializers

from core.models import Advance

class AdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance
        fields = ["id",
            "description",
            "first_line_address",
            "second_line_address",
            "postcode",
            "town_or_city",
            "reason",
            "loan_amount",
            "loan_term",
            "total_paid_already",
            "remaining_term",
            "estimated_loan_monthly_payment",
            "loan_interest_rate",
            "created_on",
            "status",
            "monthly_rent",
            "name_on_bank_account",
            "bank_account_number",
            "sort_code_bank_account",
            "is_submitting_loan",
            ]
        read_only_fields = ["id", "user_id", "created_on", "status"]
        
        # fields = "__all__"


class AdvanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance
        fields = [
            "id",
            "description",
            "reason",
            "first_line_address",
            "second_line_address",
            "postcode",
            "town_or_city",
            "country",
            "monthly_rent",
            "lease_agreement_file",
            "rent_protection_policy_file",
            "tenant_vetting_file",
            "loan_amount",
            "loan_term",
            "loan_interest_rate",
            "name_on_bank_account",
            "bank_account_number",
            "sort_code_bank_account",
            "estimated_loan_monthly_payment"
        ]

        # fields = "__all__"

