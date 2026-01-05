from django import forms
from .models import Booking, Table

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests_count', 'table', 'customer_name', 'customer_phone']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'booking-date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'id': 'booking-time'}),
            'guests_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'table': forms.HiddenInput(attrs={'id': 'selected-table-id'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (___) ___-__-__'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data