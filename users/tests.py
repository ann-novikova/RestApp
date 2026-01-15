from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from bookings.models import Booking, Table
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class UserAccountTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('users:register_api')
        self.profile_url = reverse('users:profile_api')
        self.update_url = reverse('users:profile-update')

        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Ivan',
            'last_name': 'Ivanov'
        }
        self.user = User.objects.create_user(**self.user_data)


    def test_register_user_api_success(self):
        """Тест успешной регистрации через API и получение JWT токенов"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'Sidor',
            'last_name': 'Sidorov',
            'phone': '89991112233'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(User.objects.filter(email='newuser@example.com').count(), 1)

    def test_get_user_profile_authenticated(self):
        """Тест получения данных профиля авторизованным пользователем"""
        table = Table.objects.create(number=1, capacity=4)
        Booking.objects.create(
            user=self.user,
            table=table,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            guests_count=2
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(len(response.data['bookings']), 1)
        self.assertEqual(response.data['bookings'][0]['table'], 8)


    def test_get_profile_unauthenticated(self):
        """Проверка, что неавторизованный пользователь не получит данные"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_user_profile_patch(self):
        """Тест частичного обновления данных профиля (PATCH)"""
        self.client.force_authenticate(user=self.user)
        update_data = {'first_name': 'Dmitry'}

        response = self.client.patch(self.update_url, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Dmitry')


    def test_register_html_view_post_json(self):
        """Тест RegisterHTMLView, которая принимает JSON и возвращает токены"""
        url = reverse('users:register')
        data = {
            'email': 'html_user@example.com',
            'password': 'password123',
            'first_name': 'HTML',
            'last_name': 'User'
        }
        import json
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        resp_json = response.json()
        self.assertIn('access', resp_json)
        self.assertEqual(User.objects.filter(email='html_user@example.com').count(), 1)


    def test_template_views_status_codes(self):
        """Проверка, что страницы логина и регистрации отдают 200 OK"""
        login_page = self.client.get(reverse('users:login'))
        register_page = self.client.get(reverse('users:register'))
        profile_page = self.client.get(reverse('users:profile'))

        self.assertEqual(login_page.status_code, 200)
        self.assertEqual(register_page.status_code, 200)
        self.assertEqual(profile_page.status_code, 200)

