from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm
from .models import RestaurantInfo, TeamMember


class ContentPageViewTests(TestCase):

    def setUp(self):
        """Создаем начальные данные для тестов"""
        self.info = RestaurantInfo.objects.create(
            opening_hours="11:00-23:00", address="Улица Пушкина, дом Колотушкина"
        )
        self.member = TeamMember.objects.create(
            name="Гордон Рамзи", position="Шеф-повар"
        )

    def test_home_page_status_code(self):
        """Проверка доступности главной страницы"""
        url = reverse("content:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "content/home.html")

    def test_home_page_contains_form(self):
        """Проверка наличия контактной формы в контексте"""
        url = reverse("content:home")
        response = self.client.get(url)
        self.assertIsInstance(response.context["contact_form"], ContactForm)

    def test_contact_form_submission_success(self):
        """Проверка успешной отправки контактной формы"""
        url = reverse("content:home")
        form_data = {
            "name": "Иван",
            "email": "ivan@example.com",
            "subject": "Вопрос",
            "message": "Здравствуйте, у вас есть веганское меню?",
        }
        response = self.client.post(url, data=form_data)

        self.assertRedirects(response, reverse("content:home"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Ваше сообщение успешно отправлено!")

    def test_contact_form_submission_fail(self):
        """Проверка отправки формы с некорректными данными"""
        url = reverse("content:home")
        form_data = {"name": "", "email": "not-an-email", "message": ""}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["contact_form"], "name", "This field is required."
        )

    def test_about_page_context_data(self):
        """Проверка данных о ресторане и команде на странице 'О нас'"""
        url = reverse("content:about")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "content/about.html")

        self.assertEqual(
            response.context["info"].address, "Улица Пушкина, дом Колотушкина"
        )

        self.assertIn(self.member, response.context["team"])

    def test_about_page_empty_team(self):
        """Проверка страницы, если команда еще не создана"""
        TeamMember.objects.all().delete()
        url = reverse("content:about")
        response = self.client.get(url)
        self.assertEqual(len(response.context["team"]), 0)
