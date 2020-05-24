from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required

@login_required(login_url='/user/login/')
@api_view(["GET"])
def profile_details(request):
    user=request.user
    return Response({
        'status':True,
        'user':user.to_dict()}, status=status.HTTP_200_OK)




