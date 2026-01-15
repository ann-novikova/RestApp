from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Table, Booking, RestaurantInfo
from django.contrib.auth import get_user_model

User = get_user_model()


class BookingTestCase(APITestCase):

    def setUp(self):
        """Настройка данных перед каждым тестом"""
        self.restaurant_info = RestaurantInfo.objects.create(
            opening_hours="Пн-Вс: 11:00-23:00"
        )
        self.table = Table.objects.create(number=1, capacity=4)

        self.user = User.objects.create_user(email='testuser@mail.ru', password='password123')
        self.tomorrow = timezone.now().date() + timedelta(days=1)
        self.start_time = timezone.make_aware(
            datetime.combine(self.tomorrow, datetime.strptime("12:00", "%H:%M").time()))
        self.end_time = self.start_time + timedelta(hours=1)

    def test_minimum_duration_one_hour(self):
        """Проверка правила: минимальная бронь — 1 час"""
        invalid_end_time = self.start_time + timedelta(minutes=30)
        booking = Booking(
            table=self.table,
            start_time=self.start_time,
            end_time=invalid_end_time,
            guests_count=2
        )
        with self.assertRaises(Exception):
            booking.full_clean()

    def test_booking_outside_opening_hours(self):
        """Проверка: нельзя бронировать раньше открытия (11:00)"""
        early_start = timezone.make_aware(datetime.combine(self.tomorrow, datetime.strptime("09:00", "%H:%M").time()))
        early_end = early_start + timedelta(hours=1)

        booking = Booking(
            table=self.table,
            start_time=early_start,
            end_time=early_end,
            guests_count=2
        )
        with self.assertRaises(Exception):
            booking.full_clean()


    def test_get_table_availability_success(self):
        """Проверка получения списка свободных столов"""
        url = reverse('bookings:check_availability')
        data = {
            'date': self.tomorrow.strftime('%Y-%m-%d'),
            'start': '12:00',
            'end': '13:00'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tables', response.data)

    def test_get_table_availability_missing_params(self):
        """Проверка ошибки при отсутствии параметров запроса"""
        url = reverse('bookings:check_availability')
        response = self.client.get(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_booking_as_guest(self):
        """Создание брони анонимным пользователем"""
        url = reverse('bookings:booking_create')
        data = {
            "table": self.table.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "guests_count": 2,
            "customer_name": "Иван",
            "customer_phone": "+79991234567"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertIsNone(Booking.objects.first().user)

    def test_create_booking_as_authenticated_user(self):
        """Создание брони авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        url = reverse('bookings:booking_create')
        data = {
            "table": self.table.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "guests_count": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get(id=response.data['id'])
        self.assertEqual(booking.user, self.user)

    def test_overlapping_booking_fails(self):
        """Проверка пересечения бронирований на один и тот же стол"""
        Booking.objects.create(
            table=self.table,
            start_time=self.start_time,
            end_time=self.end_time,
            guests_count=2
        )

        url = reverse('bookings:booking_create')
        data = {
            "table": self.table.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "guests_count": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
