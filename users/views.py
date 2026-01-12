from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import UserIsOwner
from .serializers import UserSerializer
from bookings.models import Booking

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response

class UserProfileView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(user=user).order_by('-start_time')
        from bookings.serializers import BookingSerializer
        booking_serializer = BookingSerializer(bookings, many=True)

        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "bookings": booking_serializer.data  # Отправляем историю вместе с профилем
        })

class UserUpdateAPIView(RetrieveUpdateAPIView):
    """Вид для обновления данных профиля"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserIsOwner]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LoginHTMLView(TemplateView):
    template_name = 'users/login.html'

class RegisterHTMLView(TemplateView):
    template_name = 'users/register.html'
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                email=data['email'],
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class ProfileHTMLView(TemplateView):
    template_name = 'users/profile.html'