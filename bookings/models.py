from django.core.validators import MinValueValidator
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
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    duration = models.PositiveIntegerField(
        default=120,
        validators=[MinValueValidator(120)],
        verbose_name="Длительность брони (мин)",
        help_text="Минимум 120 минут (2 часа)"
    )
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