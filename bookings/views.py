from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from datetime import datetime, timedelta
from .models import Table, Booking
from .serializers import BookingCreateSerializer

class TableAvailabilityView(APIView):
    """API для получения списка столиков с их статусом на конкретное время"""
    permission_classes = [permissions.AllowAny]
    template_name = 'booking.html'

    def get(self, request):
        date_str = request.query_params.get('date')
        time_str = request.query_params.get('time')

        if not date_str or not time_str:
            return Response({"error": "Date and time required"}, status=400)

        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        selected_time = datetime.strptime(time_str, '%H:%M').time()
        target_dt = datetime.combine(selected_date, selected_time)

        tables = Table.objects.all()
        table_data = []

        for table in tables:
            duration = table.min_duration
            start_search = target_dt - timedelta(minutes=duration)
            end_search = target_dt + timedelta(minutes=duration)

            # Проверка занятости
            is_occupied = Booking.objects.filter(
                table=table,
                date=selected_date,
                status__in=['pending', 'confirmed'],
                time__range=(start_search.time(), end_search.time())
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
    template_name = 'booking.html'

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCancelView(APIView):
    """Отмена брони пользователем"""
    permission_classes = [permissions.IsAuthenticated]
    template_name = 'booking.html'

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.status = 'cancelled'
            booking.save()
            return Response({"message": "Cancelled"}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
