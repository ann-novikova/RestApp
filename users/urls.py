from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig

from .views import (LoginHTMLView, ProfileHTMLView, RegisterHTMLView,
                    RegisterView, UserProfileView, UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path(
        "api/token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_api",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("api/register/", RegisterView.as_view(), name="register_api"),
    path("profile/api/", UserProfileView.as_view(), name="profile_api"),
    # HTML страницы (для браузера)
    path("login/", LoginHTMLView.as_view(), name="login"),
    path("register/", RegisterHTMLView.as_view(), name="register"),
    path("profile/", ProfileHTMLView.as_view(), name="profile"),
    path("profile/update/", UserUpdateAPIView.as_view(), name="profile-update"),
]
