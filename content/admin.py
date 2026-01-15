from django.contrib import admin

from .models import ContactMessage, RestaurantInfo, TeamMember

admin.site.register(RestaurantInfo)
admin.site.register(TeamMember)


@admin.register(ContactMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
