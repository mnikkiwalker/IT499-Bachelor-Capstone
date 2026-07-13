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
    path('confirmation/', views.confirmation_view, name='confirmation'),
]