from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactForm

class ContactCreateView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Ваше сообщение успешно отправлено!")
        return super().form_valid(form)
