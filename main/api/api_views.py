from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShopSerializer
from main.whatsapp import send_whatsapp
from main.models import Slot,Shop,Booking
from rest_framework.decorators import permission_classes, authentication_classes
from user.authentication import UserAuthentication
from user.permission import UserAccessPermission
from django.db.models import Q

class ShopView(APIView):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)
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
    try:
        shop=Shop.objects.get(gst_id=gst_id)
    except:
        return Response({
            'status': False,
            'error': 'Shop with the gst id not registered!'
        }, status=status.HTTP_404_NOT_FOUND)
    if shop==None:
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

@authentication_classes([UserAuthentication])
@permission_classes([UserAccessPermission,])
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
        slot_id=request.data['slot_id']
    except:
        return Response({
            'status':False,
            'error': 'Please send the slot id'}, status=status.HTTP_400_BAD_REQUEST)

    shop=Shop.objects.get(gst_id=shop_gst_id)
    if shop==None:
        return Response({
            'status': False,
            'error': 'Shop not found!'}, status=status.HTTP_404_NOT_FOUND)

    slot=Slot.objects.get(shop=shop, slot_id=slot_id)
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

@authentication_classes([UserAuthentication])
@permission_classes([UserAccessPermission,])
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


@authentication_classes([UserAuthentication])
@permission_classes([UserAccessPermission,])
@api_view(['GET'])
def get_shop_by_category_and_city(request, category):
    user=request.user
    payload=[]
    addresses=user.address.all()
    if not addresses.exists():
        return Response({
            'status': False,
            'error': 'Please add your address!'}, status=status.HTTP_400_BAD_REQUEST)
    for address in addresses:
        city=address.city
        shops=Shop.objects.filter(shop_city=city, shop_type=category)
        if shops.exists():
            for shop in shops:
                payload.append(shop.to_dict())
    return Response({
        'status': True,
        'payload': payload
    }, status=status.HTTP_200_OK)


@authentication_classes([UserAuthentication])
@permission_classes([UserAccessPermission,])
@api_view(['GET'])
def get_shop_by_city(request):
    user=request.user
    payload=[]
    addresses=user.address.all()
    if not addresses.exists():
        return Response({
            'status': False,
            'error': 'Please add your address!'}, status=status.HTTP_400_BAD_REQUEST)
    for address in addresses:
        city=address.city
        shops=Shop.objects.filter(shop_city=city)
        if shops.exists():
            for shop in shops:
                payload.append(shop.to_dict())
    return Response({
        'status': True,
        'payload': payload
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_for_shop(request, query):
    if query==None:
        return Response({
            'status':False,
            'error':'Empty Query'}, status=status.HTTP_400_BAD_REQUEST)
    shops=Shop.objects.filter(Q(shop_name__contains=query) | Q(shop_area__contains=query))
    payload=[]
    for shop in shops:
        payload.append(shop.to_dict())
    return Response({
        'status': True,
        'payload': payload}, status=status.HTTP_200_OK)