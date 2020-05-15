from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Slot,Shop,Booking
from .api.serializers import ShopSerializer
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from account.models import User
# Create your views here.
# #Get shops with the same pincode as the user
# @api_view(['GET'])
# def shops_near_me(request,pin):
#     shops=Shop.objects.filter(shop_pincode=pin)
#     if shops==None:
#         return Response({'msg':'No shops near the user!'}, status=status.HTTP_404_NOT_FOUND)
#
#     payload=[]
#     for shop in shops:
#         shop_dict={
#             "name":shop.shop_name,
#             "gst_id":shop.gst_id,
#             "start_time":shop.start_time,
#             "stop_time":shop.stop_time,
#             "shop_capacity":shop.shop_capacity,
#             "shop_owner_name":shop.owner_name,
#             "shop_owner_contact_number":shop.owner_phone_number,
#             "shop_address_pincode":shop.shop_pincode,
#             "shop_address_city":shop.shop_city,
#             "shop_address_area":shop.shop_area,
#             "shop_address_street":shop.shop_street,
#             "shop_address_state":shop.shop_state
#         }
#         payload.append(shop_dict)
#
#     return Response(payload, status=status.HTTP_200_OK)

class ShopView(APIView):
    def get(self, request,pin):
        qs=Shop.objects.filter(shop_pincode=pin)
        serializer=ShopSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Get the list of slots for a shop given the shops gst id
@api_view(['GET'])
def list_slots_for_shop(request, gst_id):
    shop=Shop.objects.get(gst_id=gst_id)
    slots= Slot.objects.filter(shop=shop).order_by('-slot_start_time')
    payload=[]
    for slot in slots:
        payload.append(slot.to_dict())
    return Response(payload, status=status.HTTP_200_OK)


@login_required(login_url='/accounts/login/')
@api_view(['POST'])
def book_slot(request):
    user=request.user
    try:
        shop_gst_id=request.data['gst_id']
    except:
        return Response({'error': 'Please send the shop\'s gst id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        slot_start_time=request.data['slot_start_time']
    except:
        return Response({'error': 'Please send the slot start time'}, status=status.HTTP_400_BAD_REQUEST)

    shop=Shop.objects.get(gst_id=shop_gst_id)
    if shop==None:
        return Response({'error': 'Shop not found!'}, status=status.HTTP_404_NOT_FOUND)

    slot=Slot.objects.get(shop=shop, slot_start_time=slot_start_time)
    if slot==None:
        return Response({'error': 'Slot not found!'}, status=status.HTTP_404_NOT_FOUND)

    user_bookings=user.bookings.all()
    for booking in user_bookings:
        if booking.slot==slot:
            return Response({'error': 'Only one booking per slot can be made!'}, status=status.HTTP_403_FORBIDDEN)

    book=Booking()
    book.user=user
    book.shop=shop
    book.slot=slot
    entries_left=slot.num_entries_left
    entries_left=entries_left-1
    slot.num_entries_left=entries_left
    slot.save()
    book.save()
    return Response({'msg': 'Slot booked'}, status=status.HTTP_200_OK)

@login_required(login_url='/accounts/login/')
@api_view(['GET'])
def user_booked_slots(request):
    user=request.user
    bookings=user.bookings.all()
    payload=[]
    for booking in bookings:
        payload.append(booking.slot.to_dict())

    return Response(payload, status=status.HTTP_200_OK)

class BaseView(TemplateView):
    template_name = 'home.html'


#Things left:
'''
    1. Google oAuth authorization
    2. Limiting one slot booking per user
    3. Automate slot creation
'''

# Google geocoding api to convert address into latitude longitude
# Google directions api to get directions
