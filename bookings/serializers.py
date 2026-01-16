from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Booking, Table


class TableSerializer(serializers.ModelSerializer):
    """Сериализатор для столиков"""

    class Meta:
        model = Table
        fields = ["id", "number", "capacity", "duration"]


class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор для бронирований"""

    class Meta:
        model = Booking
        fields = [
            "id",
            "table",
            "start_time",
            "end_time",
            "guests_count",
            "customer_name",
            "customer_phone",
            "status",
        ]
        read_only_fields = ["status"]

    def validate(self, attrs):
        instance = Booking(**attrs)
        try:
            instance.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs
