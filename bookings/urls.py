from django.urls import path
from bookings.apps import BookingsConfig
from .views import BookingCreateView, TableAvailabilityView, BookingCancelView, BookingPageView

app_name = BookingsConfig.name

urlpatterns = [
    path('', BookingPageView.as_view(), name='bookings'),
    path('create/', BookingCreateView.as_view(), name='booking_create'),
    path('cancel/', BookingCancelView.as_view(), name='booking_cancel'),
    path('check/', TableAvailabilityView.as_view(), name='check_availability'),

]