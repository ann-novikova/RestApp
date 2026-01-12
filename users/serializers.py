from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']
        read_only_fields = ['email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        refresh = RefreshToken.for_user(user)
        user.tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return user
