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
            "reason",
            "first_line_address",
            "second_line_address",
            "postcode",
            "town_or_city",]
        read_only_fields = ["id", "user"]


class AdvanceDetailSerializer(AdvanceSerializer):
    class Meta(AdvanceSerializer.Meta):
        fields = AdvanceSerializer.Meta.fields
        fields += ["name_on_bank_account", 
        "monthly_rent",
        # "lease_agreement_file",
        # "rent_protection_policy_file",
        # "tenant_vetting_file",
        "amount_of_rent_selling",
        "estimated_monthly_payment",
        "name_on_bank_account",
        "bank_account_number",
        "sort_code_bank_account",
        ]

