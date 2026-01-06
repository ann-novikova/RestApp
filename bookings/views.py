from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import ValidationError
from datetime import datetime
from django.shortcuts import render
from django.views import View
from .models import Table, Booking
from .serializers import BookingSerializer


class BookingPageView(View):
    def get(self, request):
        return render(request, 'booking.html')

class TableAvailabilityView(APIView):
    """API для получения списка столиков с их статусом на конкретное время"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        date_str = request.query_params.get('date')
        start_str = request.query_params.get('start')
        end_str = request.query_params.get('end')

        if not all([date_str, start_str, end_str]):
            return Response({"error": "Параметры date, start и end обязательны"}, status=400)

        try:
            start_dt = datetime.strptime(f"{date_str} {start_str}", '%Y-%m-%d %H:%M')
            end_dt = datetime.strptime(f"{date_str} {end_str}", '%Y-%m-%d %H:%M')

            Booking.validate_times(start_dt, end_dt)

        except ValidationError as e:
            return Response({"end_time": e.message}, status=400)

        tables = Table.objects.all()
        table_data = []

        for table in tables:
            is_occupied = Booking.objects.filter(
                table=table,
                status__in=['pending', 'confirmed'],
                start_time__lt=end_dt,
                end_time__gt=start_dt
            ).exists()

            table_data.append({
                'id': table.id,
                'number': table.number,
                'capacity': table.capacity,
                'is_available': not is_occupied
            })

        return Response({'tables': table_data})

class BookingCreateView(APIView):
    """Создание брони. Если есть токен — привязываем к пользователю"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCancelView(APIView):
    """Отмена брони пользователем"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.status = 'cancelled'
            booking.save()
            return Response({"message": "Cancelled"}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
