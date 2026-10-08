from django.urls import path

from .views import (
    event_create,
    event_delete,
    event_detail,
    event_list,
    event_update,
    home,
    registration_delete,
    registrations_list,
)

urlpatterns = [
    path('', home, name='home'),
    path('events/', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('events/<int:pk>/update/', event_update, name='event_update'),
    path('events/<int:pk>/delete/', event_delete, name='event_delete'),
    path('registrations/', registrations_list, name='registrations_list'),
    path('registrations/<int:pk>/delete/', registration_delete, name='registration_delete'),
]
