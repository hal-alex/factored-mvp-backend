from rest_framework import serializers

from core.models import AddressHistory

class AddressHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressHistory

        fields = ["id",
            "first_line_address",
            "second_line_address",
            "postcode",
            "town_or_city",
            "country",
            "start_date",
            "end_date",
            "duration",]
        read_only_fields = ["id", "user"]

