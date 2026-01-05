from rest_framework import serializers
from .models import Table, Booking

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'duration']

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'table', 'date', 'time', 'guests_count', 'customer_name', 'customer_phone']