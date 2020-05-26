from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from django.contrib.auth.decorators import login_required
from .models import User
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import permission_classes, authentication_classes
from user.authentication import UserAuthentication
from user.permission import UserAccessPermission
from .forms import AddressForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
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


class AddaddressView(TemplateView,LoginRequiredMixin):
    model = User, Address
    login_url = '/user/login'
    template_name = 'addaddress.html'

class ProfileView(TemplateView,LoginRequiredMixin):
    model = User
    login_url = '/user/login'
    template_name = 'profile.html'

class RegisterView(TemplateView,LoginRequiredMixin):
    model = User
    login_url = '/user/login'
    template_name = 'signup.html'

# class AddAddressView(CreateView):
#     template_name = 'addaddress.html'
#     model=Address
#     form_class = AddressForm
#     def is_valid(self,form):
#         address=form.save(commit=False)
#         address.user=User.objects.get(id=self.request.user.id)
#         address.is_main=True
#         address.save()
#         return HttpResponseRedirect('/user/user-details/')



def AddAddressView(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user= User.objects.get(id=request.user.id)
            address.is_main = True
            address.save()
            return HttpResponseRedirect('/user/profile/')
    else:
        form = AddressForm()
    return render(request, 'addaddress.html', {'form': form})