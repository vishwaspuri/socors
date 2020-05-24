from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from django.contrib.auth.decorators import login_required
from .models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404
# Create your views here.

@login_required(login_url='/user/login/')
@api_view(["POST"])
def add_address(request):
    try:
        user_id=request.data['id']
    except:
        return Response({
            'status':False,
            'error': 'User id not sent correctly!'}, status=status.HTTP_400_BAD_REQUEST)

    user=User.objects.get(id=user_id)

    if user==None:
        return Response({
            'status':False,
            'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

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
    model = User
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


