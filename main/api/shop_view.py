from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.models import Shop

@api_view(['POST'])
def shop_detail(request):
    try:
        shop_id = request.data["shop-id"]
        remark  = request.data["remark"]
        gpay    = request.data["gpay"]
        paytm   = request.data["paytm"]
        phonepe = request.data["phonepe"]
    except:
        return Response({
            "status": False,
            "detail": "Payment details or shop id not provided"
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        shop = Shop.objects.get(gst_id = shop_id)
    except:
        return Response({
            "status": False,
            "detail": "Shop doesn't exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    shop.owners_remark = remark
    shop.gpay_number = gpay
    shop.paytm_number = paytm
    shop.phonepe_number = phonepe
    shop.save()
    return Response({
        "status": True,
        "detail": "Shop details edited"
    }, status=status.HTTP_201_CREATED)