from django.contrib import admin
from .models import Table, Booking

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_active')
    list_filter = ('is_active', 'capacity')
    search_fields = ('number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start_time', 'status', 'client', 'guests_count')
    list_editable = ('status',)
    list_filter = ('status', 'table', 'start_time')
    search_fields = ('customer_name', 'customer_phone', 'user__first_name', 'user__email')
    ordering = ('-start_time',)

    actions = ['confirm', 'cancel']

    @admin.action(description="Подтвердить выбранные")
    def confirm(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description="Отменить выбранные")
    def cancel(self, request, queryset):
        queryset.update(status='cancelled')

    @admin.display(description="Клиент")
    def client(self, obj):
        return obj.user or f"{obj.customer_name} ({obj.customer_phone})"

    fields = ('status', 'table', 'guests_count', ('start_time', 'end_time'), 'user', ('customer_name', 'customer_phone'))