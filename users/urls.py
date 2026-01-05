from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from .views import RegisterView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
