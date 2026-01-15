from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking, Table


class BookingService:
    @staticmethod
    def get_table_availability(date_str: str, start_str: str, end_str: str):
        """
        Получает список столиков и их доступность на заданный период.
        Возвращает список словарей с данными о столиках.
        """
        try:
            start_dt = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")

            if timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt)
            if timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt)

            Booking.validate_times(start_dt, end_dt)

        except ValidationError as e:
            raise ValidationError({"end_time": e.message})
        except ValueError:
            raise ValidationError(
                "Неверный формат даты или времени. Используйте YYYY-MM-DD HH:MM."
            )

        tables = Table.objects.all()
        table_data = []

        overlapping_bookings = Booking.objects.filter(
            status__in=["confirmed"], start_time__lt=end_dt, end_time__gt=start_dt
        )

        for table in tables:
            is_occupied = overlapping_bookings.filter(table=table).exists()

            table_data.append(
                {
                    "id": table.id,
                    "number": table.number,
                    "capacity": table.capacity,
                    "is_available": not is_occupied,
                }
            )

        return table_data
