from django.urls import path
from bookings.apps import BookingsConfig
from .views import BookingCreateView, TableAvailabilityView, BookingCancelView

app_name = BookingsConfig.name

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking_create'),
    path('cancel/', BookingCancelView.as_view(), name='booking_cancel'),
    path('check/', TableAvailabilityView.as_view(), name='check_availability'),

]