from django.urls import path

from bookings.apps import BookingsConfig

from .views import BookingCreateView, BookingPageView, TableAvailabilityView

app_name = BookingsConfig.name

urlpatterns = [
    path("", BookingPageView.as_view(), name="bookings"),
    path("create/", BookingCreateView.as_view(), name="booking_create"),
    path("check/", TableAvailabilityView.as_view(), name="check_availability"),
]
