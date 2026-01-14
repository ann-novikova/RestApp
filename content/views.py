from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .models import RestaurantInfo, TeamMember
from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'contact_form' not in context:
            context['contact_form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('content:home')
        else:
            context = self.get_context_data(**kwargs)
            context['contact_form'] = contact_form
            return render(request, self.template_name, context)

class AboutView(TemplateView):
    template_name = 'content/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = RestaurantInfo.objects.first()
        context['team'] = TeamMember.objects.all()
        return context