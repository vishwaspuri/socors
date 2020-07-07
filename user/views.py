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
from .forms import AddressForm, ProfileUpdateForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .addresshelper import make_prior_address_not_main
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
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

@login_required
def update_profile(request):
    if request.method =="POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect('/user/profile/')
        else:
            errors = form.errors
            # print(errors)
            return render(request, 'edit_profile.html', {
                'errors': errors
            })
    else:
        form = ProfileUpdateForm()
        return render(request, 'edit_profile.html', {
            'form': form
        })

@login_required
def change_main_address(request):
    if request.method=="POST":
        # print(request.POST)
        try:
            pk_address=request.POST['selectedAddress']
        except:
            return redirect('/user/profile/')
        address = Address.objects.get(id = pk_address)
        # print(address.city)
        make_prior_address_not_main(request.user.id)
        address.is_main = True
        address.save()
        return redirect('/user/profile/')
    else:
        return render(request, 'profile.html')


def remove_address(request):
    if request.method == 'POST':
        try:
            address_id = request.POST['address_pk']
        except:
            return redirect('/user/profile/')
        address = Address.objects.get(id = address_id)
        if address.is_main == True:
            # Find a new address and make it main
            # print("Main address reached")
            new_main_address = Address.objects.filter(user= request.user).first()
            # print(new_main_address.city)
            if new_main_address != None:
                new_main_address.is_main = True
                new_main_address.save()
        print(address)
        address.delete()
        return redirect('/user/profile/')

@login_required
def edit_address(request):
    if request.method=='POST':
        address = Address.objects.get(id = request.POST['address_id'])
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('/user/profile/')


def login_view(request):
    if request.method == "POST":
        ph_number = request.POST['ph_number']
        password  = request.POST['password']
        try:
            email = User.objects.get(ph_number= ph_number).email
        except KeyError:
            return redirect(request, 'login.html')
            # return redirect(request, 'login.html', {
            #     "is_valid": False,
            #     "error": "The phone number entered does not exist."
            # })
        user = authenticate(username = email, password= password)
        if user is not None:
            if user.is_active:
                login(request, user=user)
                return redirect('main:explore')
            else:
                return HttpResponseForbidden("<html><head><title>Login Forbidden</title></head><body><h1>The User is deactivated. Please contact customer service.</h1></body></html>")
        else:
            return redirect(request, 'login.html', {
                "is_valid": False,
                "error": "Invalid credentials provided"
            })
    else:
        return render(request, 'login.html')
