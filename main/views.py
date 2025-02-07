from user.models import User
from main.models import Shop,Slot,BuyInBooking, PickUpBooking, PickUpNotification
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from .forms import PickUpForm
from main.shopkeeper_helpers import send_pick_up_to_shopkeeper, send_buy_in_to_shopkeeper
from datetime import datetime, timedelta
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

class MytimeslotsView(LoginRequiredMixin,TemplateView):
    model = User, Shop, Slot, BuyInBooking,PickUpBooking
    login_url = '/user/login/'
    template_name = 'mytimeslots.html'



# ----------------------------------------------------------------
# -----------------ACTION VIEWS-----------------------------------
# ----------------------------------------------------------------

def pick_up_view(request, slot_id):
    if request.method == 'POST':
        data = request.POST.dict()
        items_dict      = {k:v for (k,v) in data.items() if k.startswith('item')}
        quantity_dict   = {k:v for (k,v) in data.items() if k.startswith('qty')}
        remark_dict     = {k:v for (k,v) in data.items() if k.startswith('remark')}
        order = 'Order is\n'
        for key,item in items_dict.items():
            key_number = key[4:]
            quatity_name = 'qty'+str(key_number)
            remark_name  = 'remark'+str(key_number)
            if quatity_name in quantity_dict:
                quantity = quantity_dict[quatity_name]
            else:
                quantity = 'N/A'
            if  remark_name in remark_dict:
                remark = remark_dict[remark_name]
            else:
                remark = 'N/A'
            order = order + 'Item:' + str(item) + ' Quantity:' + str(quantity) + ' Remark:' + str(remark) + '\n'
        # print(order)
        if request.POST['Delivery']=='1':
            is_delivery = True
        else:
            is_delivery = False
        slot = Slot.objects.get(slot_id=slot_id)
        pickup = PickUpBooking()
        pickup.user = request.user
        pickup.slot = slot
        pickup.shop = slot.shop
        pickup.message_for_shopkeeper = order
        pickup.is_delivery = is_delivery
        pickup.save()
        send_pick_up_to_shopkeeper(is_delivery,str(slot.slot_id), str(pickup.pick_up_id), str(pickup.user.id), str(pickup.user.full_name), str(pickup.message_for_shopkeeper))

        url = reverse('main:my-timeslots-post-confirmation', kwargs={'slot_id': slot.slot_id})
        return HttpResponseRedirect(url)
    else:
        print("1")
        try:
            slot = Slot.objects.get(slot_id=slot_id)
            if (request.GET.get('delivery') == 'True'):
                return render(request, 'pickupform.html', {
                    'is_delivery': True,
                    "slot_id": slot.slot_id
                })
            else:
                return render(request, 'pickupform.html', {"slot_id": slot.slot_id})
        except:
            slot = Slot.objects.get(slot_id=slot_id)
            return render(request, 'pickupform.html', {"slot_id": slot.slot_id})



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
    if shop.stop_time < datetime.today().time():
        tomorrow = datetime.today()+timedelta(days=1)
        slots = Slot.objects.filter(
            shop= shop,
            slot_start_time__day= tomorrow.day,
            slot_stop_time__month= tomorrow.month,
        )
        return render(request, 'shopslots.html', {'slots': slots, 'shop': shop, 'date': tomorrow.date()})
    else:
        slots=Slot.objects.filter(
            shop=shop,
            slot_start_time__day = datetime.today().day,
            slot_start_time__month = datetime.today().month,
            is_break=False)
        return render(request, 'shopslots.html', {'slots':slots, 'shop': shop, 'date': datetime.today().date()})

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
            url = reverse('main:my-timeslots-post-confirmation', kwargs={'slot_id': slot.slot_id})
            return HttpResponseRedirect(url)

def create_pick_up_booking(request, slot_id):
    if request.method == "POST":
        print(request.POST)
        form = PickUpForm(request.POST)
        if form.is_valid():
            pickup      = form.save(commit=False)
            pickup.user = request.user
            slot        = Slot.objects.get(slot_id=slot_id)
            pickup.slot = slot
            pickup.shop = slot.shop
            pickup.save()
            send_pick_up_to_shopkeeper(str(slot.slot_id), str(pickup.pick_up_id), str(pickup.user.id), str(pickup.user.full_name), str(pickup.message_for_shopkeeper))
            return HttpResponseRedirect('/mytimeslots')
    else:
        form = PickUpForm()
    # Check whether delivery is true
    '''
    print("1")
    try:
        print("Idhar to pahuncha")
        if(request.GET.get('delivery') == 'True'):
            return render(request, 'shopslots.html', {
                'is_delivery': True,
                'form': form
            })
    except:
    '''
    return render(request, 'shopslots.html', {
        'form': form
    })


def my_timeslots_post_confirmation(request,slot_id):
    fin_slot = Slot.objects.get(slot_id=slot_id)
    return render(request, 'mytimeslotswithconfirmation.html', {
        "fin_slot":fin_slot
    })


