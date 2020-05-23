from django.urls import path
from user.api import auth
from django.contrib.auth.views import LoginView, LogoutView
from .views import add_address, AddaddressView, ProfileView, RegisterView
from .api.auth import ValidatePhoneSendOTP, validateOTP
from .api.api_views import profile_details

urlpatterns = [
    path('auth/login/', auth.login, name='api-login'),
    path('auth/register/', auth.register, name='api-register'),
    path('login/',LoginView.as_view(
        template_name='login.html'
    ), name='login'),
    path('api/new-address/',add_address, name='add-address/'),
    path('api/validate-phone/',  ValidatePhoneSendOTP.as_view(), name='validate-phone-number'),
    path('api/otp', validateOTP.as_view(), name='validate-otp'),
    path('add-address/', AddaddressView.as_view(), name='add-address'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('user-details/', profile_details, name='user-details'),
    path('logout/', LogoutView.as_view(
        next_page='/'
    ),name='logout')
]