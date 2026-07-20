"""
this file is for url paths nested under our appointment app.
Think of this as any urls that would look like:
"https://www.ourapp.com/appointments/[APPS HERE]
"""

from django.urls import path
from . import views

app_name = "appointment"

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('schedule/add/', views.save_appt, name='save_appt'),
    path('confirmation/<int:slot_id>', views.confirmation_view, name='confirmation'),
]