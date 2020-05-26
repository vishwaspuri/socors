from user.models import User
from main.models import Shop,Slot,BuyInBooking, PickUpBooking, PickUpNotification
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PickUpForm
# ------------------------------------------------------------------------------
# -----------------GENERIC VIEWS FOR TEMPLATES----------------------------------
# ------------------------------------------------------------------------------

class BaseView(TemplateView,LoginRequiredMixin):
    login_url = '/user/login'
    template_name = 'home.html'

class MenuView(TemplateView,LoginRequiredMixin):
    model=User, Shop, Slot
    login_url = '/user/login'
    template_name = 'menu.html'

class NotificationView(TemplateView,LoginRequiredMixin):
    model = User, Shop, Slot, PickUpNotification
    login_url = '/user/login'
    template_name = 'notifications.html'

class MytimeslotsView(TemplateView,LoginRequiredMixin):
    model = User, Shop, Slot, BuyInBooking,PickUpBooking
    login_url = '/user/login'
    template_name = 'mytimeslots.html'

# ----------------------------------------------------------------
# -----------------ACTION VIEWS-----------------------------------
# ----------------------------------------------------------------


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
    if not address.exists():
        return HttpResponseRedirect('user/add-address/')
    city=address.city
    shops=Shop.objects.filter(shop_city=city, shop_type=cat)
    return render(request, 'shopsnearme.html', {'shops':shops})

def create_buy_in_booking(request, slot_id):
    slot = Slot.objects.get(slot_id=slot_id)
    user = request.user
    shop = slot.shop
    if slot.num_entries_left:
        slot.num_entries_left=slot.num_entries_left-1
        slot.save()
        BuyInBooking(slot=slot, shop=shop, user=user)
        return HttpResponseRedirect('/mytimeslots/')

def create_pick_up_booking(request, slot_id):
    if request.method == "POST":
        form = PickUpForm(request.POST)
        if form.is_valid():
            pickup      = form.save(commit=False)
            pickup.user = request.user
            slot        = Slot.objects.get(slot_id=slot_id)
            pickup.slot = slot
            pickup.shop = slot.shop
            pickup.save()
            return HttpResponseRedirect('/mytimeslots/')
    else:
        form = PickUpForm()
    return render(request, 'shopslots.html', {'form': form})