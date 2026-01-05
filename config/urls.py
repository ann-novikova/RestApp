from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("content.urls")),
    path("users/", include("users.urls", namespace="users")),
    path("bookings/", include("bookings.urls", namespace="bookings")),
]
