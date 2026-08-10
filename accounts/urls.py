from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_not_required
from . import views


app_name = "account"

urlpatterns = [
    path('', 
        login_not_required(
            LoginView.as_view(template_name='accounts/login.html'),
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', views.search_api, name='search_api')
]