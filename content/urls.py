from django.urls import path

from content.apps import ContentConfig

from .views import AboutView, HomeView

app_name = ContentConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
]
