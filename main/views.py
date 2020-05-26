from user.models import User
from main.models import Shop,Slot,Booking
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.authentication import UserAuthentication
from user.permission import UserAccessPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# ----------------------------------------------------------------
# -----------------GENERIC VIEWS----------------------------------
# ----------------------------------------------------------------

class BaseView(TemplateView,LoginRequiredMixin):
    login_url = '/user/login'
    template_name = 'home.html'

class MenuView(TemplateView,LoginRequiredMixin):
    model=User, Shop, Slot, Booking
    login_url = '/user/login'
    template_name = 'menu.html'

class NotificationView(TemplateView,LoginRequiredMixin):
    model = User, Shop, Slot, Booking
    login_url = '/user/login'
    template_name = 'notifications.html'

class MytimeslotsView(TemplateView,LoginRequiredMixin):
    model = User, Shop, Slot, Booking
    login_url = '/user/login'
    template_name = 'mytimeslots.html'



def shop_near_me(request):
    user=request.user
    pin = 0
    for address in user.address.all():
        if address.is_main:
            pin=address.pincode
    shops=Shop.objects.filter(shop_pincode__exact=int(pin))
    return render(request, 'shopsnearme.html', {'shops':shops})

def shop_slots(request,gst_id):
    shop=Shop.objects.get(gst_id=gst_id)
    slots=Slot.objects.filter(shop=shop)
    return render(request, 'shopslots.html', {'slots':slots})

def shop_by_cat(request, cat):
    user=request.user
    address=user.address.get(is_main=True)
    city=address.city
    shops=Shop.objects.filter(shop_city=city, shop_type=cat)
    return render(request, 'shopsnearme.html', {'shops':shops})