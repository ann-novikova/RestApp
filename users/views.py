from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer, UserBookingHistorySerializer
from bookings.models import Booking

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

class UserProfileView(ListAPIView):
    """Список бронирований текущего пользователя (Личный кабинет)"""
    serializer_class = UserBookingHistorySerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-date')