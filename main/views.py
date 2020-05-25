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

class ExploreView(TemplateView,LoginRequiredMixin):
    model = User, Shop, Slot, Booking
    login_url = '/user/login'
    template_name = 'shopsnearme.html'


def shop_near_me(request):
    user=request.user
    pin = 0
    for address in user.address.all():
        if address.is_main:
            pin=address.pincode
    print(pin)
    shops=Shop.objects.filter(shop_pincode__exact=int(pin))
    for shop in shops:
        print(shop.shop_name)
    return render(request, 'shopsnearme.html', {'shops':shops})


class SlotsView(TemplateView,LoginRequiredMixin):
    model = User, Shop, Slot, Booking
    login_url = '/user/login'
    template_name = 'shopslots.html'


class TestView(APIView):
    """
    Returns home text if the user is authenticated successfully and has permissions.
    **Example requests**:
        GET /api/home/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    def get(self, request):
        content = {
            'message': 'Welcome '
        }
        return Response(content, status=status.HTTP_200_OK)