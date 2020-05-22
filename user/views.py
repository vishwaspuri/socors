from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from django.contrib.auth.decorators import login_required
from .models import User

from django.shortcuts import get_object_or_404
# Create your views here.

@login_required(login_url='/accounts/login/')
@api_view(["POST"])
def add_address(request):
    try:
        user_id=request.data['id']
    except:
        return Response({'error': 'User id not sent correctly!'}, status=status.HTTP_400_BAD_REQUEST)

    user=User.objects.get(id=user_id)

    if user==None:
        return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

    try:
        city=request.data['city']
    except:
        return Response({'error': 'City not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        area=request.data['area']
    except:
        return Response({'error': 'Address area not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        street=request.data['street']
    except:
        return Response({'error': 'Street not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        state=request.data['state']
    except:
        return Response({'error': 'State not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pincode=request.data['pincode']
    except:
        return Response({'error': 'Pincode not sent!'}, status=status.HTTP_400_BAD_REQUEST)

    address=Address()
    address.city=city
    address.area=area
    address.street=street
    address.state=state
    address.pincode=pincode
    address.save()

    return Response(address.to_dict(), status=status.HTTP_201_CREATED)


