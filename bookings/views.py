from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Table
from .serializers import BookingSerializer, TableSerializer
from .services import BookingService


class BookingPageView(View):
    """Отображает страницу бронирования (не API)"""

    def get(self, request):
        return render(request, "booking.html")


class TableAvailabilityView(ListAPIView):
    """API для получения списка столиков с их статусом на конкретное время"""

    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Table.objects.all()

    def get(self, request):
        date_str = request.query_params.get("date")
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")

        if not all([date_str, start_str, end_str]):
            return Response(
                {"error": "Параметры date, start и end обязательны"}, status=400
            )

        try:
            table_data = BookingService.get_table_availability(
                date_str, start_str, end_str
            )
            return Response({"tables": table_data})

        except ValidationError as e:
            return Response(
                {"errors": e.message_dict or e.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"Error in TableAvailabilityView: {e}")
            return Response(
                {
                    "error": "Произошла внутренняя ошибка при получении данных о столиках"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BookingCreateView(APIView):
    """Создание брони. Если есть токен — привязываем к пользователю"""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = request.user if request.user.is_authenticated else None
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            error_message = ""
            if hasattr(e, "message_dict"):
                error_message = " ".join([f"{v[0]}" for k, v in e.message_dict.items()])
            else:
                error_message = e.messages[0]

            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print(f"Error saving booking: {e}")
            return Response(
                {"error": "Произошла внутренняя ошибка при сохранении"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
