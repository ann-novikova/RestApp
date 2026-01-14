from django.db import models
from solo.models import SingletonModel


class RestaurantInfo(SingletonModel):
    """Модель для описания общей информации о ресторане"""

    name = models.CharField(max_length=255, verbose_name="Название ресторана")
    image = models.ImageField(upload_to="content/resto/", verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание ресторана")
    address = models.CharField(max_length=255, verbose_name="Адрес ресторана")
    phone = models.CharField(max_length=20, verbose_name="Телефон ресторана")
    email = models.EmailField(verbose_name="Email ресторана")
    opening_hours = models.TextField(
        null=True,
        blank=True,
        verbose_name="Рабочие часы",
        help_text="Пн-Вс: 11:00-23:00",
    )
    about_history = models.TextField(
        null=True, blank=True, verbose_name="История ресторана"
    )
    about_mission = models.TextField(
        null=True, blank=True, verbose_name="Миссия ресторана"
    )
    team_description = models.TextField(
        null=True, blank=True, verbose_name="Описание команды"
    )

    class Meta:
        verbose_name = "Информация о ресторане"
        verbose_name_plural = "Информация о ресторане"

    def __str__(self):
        """Возвращает строковое представление объекта Ресторана"""
        return self.name

class TeamMember(models.Model):
    """Модель для описания членов команды ресторана"""

    name = models.CharField(max_length=255, verbose_name="Имя")
    position = models.CharField(max_length=255, verbose_name="Должность")
    bio = models.TextField(null=True, blank=True, verbose_name="Подробности")
    photo = models.ImageField(upload_to="content/team/", verbose_name="Фото")

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Команда"

    def __str__(self):
        """Возвращает строковое представление объекта TeamMember"""
        return f'{self.name} - {self.position}'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата получения")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"От {self.name} - {self.subject}"



