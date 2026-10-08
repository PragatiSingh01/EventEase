from django.contrib import admin

from .models import Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'venue', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'venue')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event', 'department', 'email', 'created_at')
    list_filter = ('department', 'event')
    search_fields = ('full_name', 'email', 'event__title')
