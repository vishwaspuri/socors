from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShopSerializer
from django.contrib.auth.decorators import login_required
from main.whatsapp import send_whatsapp
from main.models import Slot,Shop,Booking
from django.contrib.auth.mixins import LoginRequiredMixin

class ShopView(APIView, LoginRequiredMixin):
    login_url = '/user/login/'
    def get(self, request,pin):
        user=request.user
        user_addresses=user.address.all()
        if user_addresses==None:
            return Response({
                'status': False,
                'error': 'User must add address first'
            }, status=status.HTTP_404_NOT_FOUND)
        qs=Shop.objects.filter(shop_pincode=pin)
        serializer=ShopSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Get the list of slots for a shop given the shops gst id
@api_view(['GET'])
def list_slots_for_shop(request, gst_id):
    shop=Shop.objects.get(gst_id=gst_id)
    if not shop.exists():
        return Response({
            'status': False,
            'error': 'Shop with the gst id not registered!'
        }, status=status.HTTP_404_NOT_FOUND)
    slots= Slot.objects.filter(shop=shop).order_by('-slot_start_time')
    if not slots.exists():
        return Response({
            'status': False,
            'error': 'Shop does not have more slots!'
        }, status=status.HTTP_404_NOT_FOUND)
    payload=[]
    for slot in slots:
        payload.append(slot.to_dict())
    return Response({
        'status':True,
        'payload':payload}, status=status.HTTP_200_OK)

@login_required(login_url='/user/login/')
@api_view(['POST'])
def book_slot(request):
    user=request.user
    try:
        shop_gst_id=request.data['gst_id']
    except:
        return Response({
            'status':False,
            'error': 'Please send the shop\'s gst id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        slot_start_time=request.data['slot_start_time']
    except:
        return Response({
            'status':False,
            'error': 'Please send the slot start time'}, status=status.HTTP_400_BAD_REQUEST)

    shop=Shop.objects.get(gst_id=shop_gst_id)
    if shop==None:
        return Response({
            'status': False,
            'error': 'Shop not found!'}, status=status.HTTP_404_NOT_FOUND)

    slot=Slot.objects.get(shop=shop, slot_start_time=slot_start_time)
    if slot==None:
        return Response({
            'status':False,
            'error': 'Slot not found!'}, status=status.HTTP_404_NOT_FOUND)

    user_bookings=user.bookings.all()
    for booking in user_bookings:
        if booking.slot==slot:
            return Response({
                'status': False,
                'error': 'Only one booking per slot can be made!'}, status=status.HTTP_403_FORBIDDEN)
    if shop.give_whatsapp_order==False:
        book = Booking()
        book.user = user
        book.shop = shop
        book.slot = slot
        entries_left = slot.num_entries_left
        entries_left = entries_left - 1
        slot.num_entries_left = entries_left
        slot.save()
        book.save()
        return Response({
            'status':True,
            'msg': 'Slot booked'}, status=status.HTTP_200_OK)
    else:
        try:
            message=request.data['message']
            message='Mr./Mrs. '+str(user.first_name)+' has the following order:\n'+message
            book = Booking()
            book.user = user
            book.shop = shop
            book.slot = slot
            book.message_for_shopkeeper = message
            flag=send_whatsapp(user.ph_number, message)
            entries_left = slot.num_entries_left
            entries_left = entries_left - 1
            slot.num_entries_left = entries_left
            slot.save()
            book.save()
            if flag:
                return Response({
                    'status':True,
                    'msg': 'Slot booked'}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': True,
                    'msg': 'Slot booked but message could not be sent!'}, status=status.HTTP_200_OK)
        except:
            book = Booking()
            book.user = user
            book.shop = shop
            book.slot = slot
            entries_left = slot.num_entries_left
            entries_left = entries_left - 1
            slot.num_entries_left = entries_left
            slot.save()
            book.save()
            return Response({
                'status':True,
                'msg': 'Slot booked'}, status=status.HTTP_200_OK)

@login_required(login_url='/user/login/')
@api_view(['GET'])
def user_booked_slots(request):
    try:
        user=request.user
    except:
        return Response({
                'status': False,
                'detail': 'User not authenticated!'
            }, status=status.HTTP_403_FORBIDDEN)
    bookings=user.bookings.all()
    if bookings==None:
        return Response({
            'status': False,
            'detail': 'User has no bookings yet!'
        }, status=status.HTTP_404_NOT_FOUND)
    payload=[]
    for booking in bookings:
        payload.append(booking.slot.to_dict())

    return Response({
        'status':True,
        'payload':payload}, status=status.HTTP_200_OK)