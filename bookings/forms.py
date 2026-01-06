from django import forms
from .models import Booking, Table

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['table', 'start_time', 'end_time', 'guests_count', 'customer_name', 'customer_phone']