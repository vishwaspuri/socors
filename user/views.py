from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from .models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import permission_classes, authentication_classes
from user.authentication import UserAuthentication
from user.permission import UserAccessPermission
from .forms import AddressForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .addresshelper import make_prior_address_not_main
# Create your views here.

@authentication_classes([UserAuthentication])
@permission_classes([UserAccessPermission])
@api_view(["POST"])
def add_address(request):
    user=request.user

    try:
        city=request.data['city']
    except:
        return Response({
            'status':False,
            'error': 'City not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        area=request.data['area']
    except:
        return Response({
            'status':False,
            'error': 'Address area not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        street=request.data['street']
    except:
        return Response({
            'status':False,
            'error': 'Street not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        state=request.data['state']
    except:
        return Response({
            'status': False,
            'error': 'State not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pincode=request.data['pincode']
    except:
        return Response({
            'status':False,
            'error': 'Pincode not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    address=Address()
    address.user=user
    address.city=city
    address.area=area
    address.street=street
    address.state=state
    address.pincode=pincode
    address.save()

    return Response({
        'status':True,
        'address':address.to_dict()}, status=status.HTTP_201_CREATED)


class AddaddressView(LoginRequiredMixin,TemplateView):
    model = User, Address
    login_url = '/user/login'
    template_name = 'addaddress.html'

class AfterAddressView(LoginRequiredMixin,TemplateView):
    model = User, Address
    login_url = '/user/login'
    template_name = 'afteraddressprofile.html'


class ProfileView(LoginRequiredMixin,TemplateView):
    model = User
    login_url = '/user/login'
    template_name = 'profile.html'

class RegisterView(TemplateView):
    model = User
    login_url = '/user/login'
    template_name = 'signup.html'


def AddAddressView(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            make_prior_address_not_main(request.user.id)
            address = form.save(commit=False)
            address.user= User.objects.get(id=request.user.id)
            address.is_main = True
            address.save()
            return HttpResponseRedirect('/user/after-address-profile/')
    else:
        form = AddressForm()
    return render(request, 'addaddress.html', {'form': form})

class PrivacyPolicyView(TemplateView):
    template_name='privacy_policy.html'

class TermsConditionsView(TemplateView):
    template_name='terms_and_conditions.html'