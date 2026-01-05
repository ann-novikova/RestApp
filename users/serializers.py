from rest_framework import serializers
from .models import User
from bookings.models import Booking

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserBookingHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для отображения истории бронирований в профиле"""
    table_number = serializers.ReadOnlyField(source='table.number')

    class Meta:
        model = Booking
        fields = ['id', 'table_number', 'date', 'time', 'duration','status']
