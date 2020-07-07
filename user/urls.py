from django.urls import path
from user.api import auth
from django.contrib.auth.views import LogoutView, LoginView
from .views import login_view, edit_address, remove_address, change_main_address, update_profile, add_address, AddaddressView, ProfileView, RegisterView,AddAddressView, AfterAddressView, TermsConditionsView, PrivacyPolicyView
from .api.auth import ValidatePhoneSendOTP, validateOTP
from .api.api_views import profile_details

urlpatterns = [
    path('api/login/', auth.LoginView.as_view(), name='api-login'),
    # path('login/', LoginView.as_view(
    #     template_name='login.html'
    # ), name='login'),
    path('login/', login_view, name="login"),
    path('api/new-address/',add_address, name='add-address/'),
    path('api/validate-phone/',  ValidatePhoneSendOTP.as_view(), name='validate-phone-number'),
    path('api/otp/', validateOTP.as_view(), name='validate-otp'),
    path('api/add-address/', AddaddressView.as_view(), name='api-add-address'),
    path('after-address-profile/', AfterAddressView.as_view(), name='after-address'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('api/user-details/', profile_details, name='user-details'),
    path('logout/', LogoutView.as_view(
        next_page='/'
    ),name='logout'),
    path('add-address/', AddAddressView, name='add-address'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsConditionsView.as_view(), name='terms-n-conditions'),
    path('update-profile/', update_profile, name='update-profile'),
    path('change-main-address/', change_main_address, name='change-main-address'),
    path('remove-address/', remove_address, name='remove-address'),
    path('edit-address/', edit_address, name='edit-address')
]