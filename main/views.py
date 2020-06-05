from user.models import User
from main.models import Shop,Slot,BuyInBooking, PickUpBooking, PickUpNotification
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PickUpForm
from main.shopkeeper_helpers import send_pick_up_to_shopkeeper, send_buy_in_to_shopkeeper

# ------------------------------------------------------------------------------
# -----------------GENERIC VIEWS FOR TEMPLATES----------------------------------
# ------------------------------------------------------------------------------

class BaseView(TemplateView):
    login_url = '/user/login/'
    template_name = 'home.html'

class MenuView(LoginRequiredMixin,TemplateView):
    model=User, Shop, Slot
    login_url = '/user/login/'
    template_name = 'menu.html'

class NotificationView(LoginRequiredMixin,TemplateView):
    model = User, Shop, Slot, PickUpNotification
    login_url = '/user/login/'
    template_name = 'notifications.html'

class MytimeslotsView(LoginRequiredMixin,TemplateView):
    model = User, Shop, Slot, BuyInBooking,PickUpBooking
    login_url = '/user/login/'
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
    return render(request, 'shopslots.html', {'slots':slots, 'shop': shop})

def shop_by_cat(request, cat):
    user=request.user
    try:
        address=user.address.get(is_main=True)
    except:
        return HttpResponseRedirect('/user/add-address/')
    city=address.city
    shops=Shop.objects.filter(shop_city=city, shop_type=cat)
    return render(request, 'shopsnearme.html', {'shops':shops})

def create_buy_in_booking(request, slot_id):
    if request.method== "POST":
        slot = Slot.objects.get(slot_id=slot_id)
        user = request.user
        shop = slot.shop
        slot.num_entries_left=slot.num_entries_left-1
        slot.save()
        try:
            buyin = BuyInBooking.objects.get(slot=slot, user=user)
            return HttpResponseRedirect('/mytimeslots/')
        except:
            buyin=BuyInBooking()
            buyin.user=user
            buyin.slot=slot
            buyin.shop=shop
            buyin.save()
            print(buyin.buy_in_id)
            send_buy_in_to_shopkeeper(str(slot.slot_id), str(buyin.buy_in_id), str(user.id), str(user.full_name))
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
            send_pick_up_to_shopkeeper(str(slot.slot_id), str(pickup.pick_up_id), str(pickup.user.id), str(pickup.user.full_name), str(pickup.message_for_shopkeeper))
            return HttpResponseRedirect('/mytimeslots/')
    else:
        form = PickUpForm()
    return render(request, 'shopslots.html', {'form': form})