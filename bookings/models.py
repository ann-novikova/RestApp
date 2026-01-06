from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from django.db import models

from config import settings


class Table(models.Model):
    """Модель столика"""

    number = models.PositiveSmallIntegerField(
        unique=True,
        validators=[MinValueValidator(1)],
        verbose_name="Номер столика"
    )
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Вместимость (чел.)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Доступен для бронирования")

    class Meta:
        ordering = ['number']
        verbose_name = "Столик"
        verbose_name_plural = "Столики"

    def __str__(self):
        return f"Столик №{self.number} (на {self.capacity} чел.)"


class Booking(models.Model):
    """Модель для бронирования столиков"""

    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True, blank=True,
        verbose_name="Пользователь"
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Столик"
    )
    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    guests_count = models.PositiveSmallIntegerField(verbose_name="Количество гостей")

    # Данные для гостей без регистрации
    customer_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    customer_phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронь №{self.id} - Столик {self.table.number} на {self.date}"

    @staticmethod
    def validate_times(start_time, end_time):
        """Единая логика проверки времени для всех мест"""
        if not start_time or not end_time:
            raise ValidationError("Необходимо указать начало и конец.")

        if start_time >= end_time:
            raise ValidationError("Время окончания должно быть позже начала.")

        if (end_time - start_time) < timedelta(hours=2):
            raise ValidationError("Минимальное время бронирования — 2 часа.")

        return True

    def clean(self):
        """
        Единая валидация для форм, админки и API
        """
        # 1. Проверка времени
        self.validate_times(self.start_time, self.end_time)

        # 2. Проверка столика и гостей
        if self.table and self.guests_count:
            if self.guests_count > self.table.capacity:
                raise ValidationError({
                    'guests_count': f"Стол №{self.table.number} вмещает только {self.table.capacity} чел."
                })

        # 3. Проверка пересечений
        if self.table and self.start_time and self.end_time:
            overlapping = Booking.objects.filter(
                table=self.table,
                status__in=['pending', 'confirmed'],
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError("Этот столик уже занят на это время.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)