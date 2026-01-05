from django.views.generic import TemplateView
from .models import RestaurantInfo, TeamMember
from feedback.forms import ContactForm

class HomeView(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = RestaurantInfo.objects.first()
        context['form'] = ContactForm()
        return context

class AboutView(TemplateView):
    template_name = 'content/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = RestaurantInfo.objects.first()
        context['team'] = TeamMember.objects.all()
        return context