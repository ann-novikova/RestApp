from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Table, Booking

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'duration']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'table', 'start_time', 'end_time',
            'guests_count', 'customer_name', 'customer_phone', 'status'
        ]
        read_only_fields = ['status']

    def validate(self, attrs):
        instance = Booking(**attrs)
        try:
            instance.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs