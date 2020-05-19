from django.urls import path
from account.api import auth
from django.contrib.auth.views import LoginView
from .views import add_address

urlpatterns = [
    path('auth/login/', auth.login, name='api-login'),
    path('auth/register/', auth.register, name='api-register'),
    path('login/',LoginView.as_view(
        template_name='login.html'
    ), name='login'),
    path('api/new-address/',add_address, name='add-address' )
]