from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email"]
        read_only_fields = ["email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)

        refresh = RefreshToken.for_user(user)
        user.tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return user
