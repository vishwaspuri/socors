from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes
from user.authentication import UserAuthentication
from user.permission import UserAccessPermission

@authentication_classes([UserAuthentication])
@permission_classes([UserAccessPermission])
@api_view(["GET"])
def profile_details(request):
    user=request.user
    return Response({
        'status':True,
        'user':user.to_dict()}, status=status.HTTP_200_OK)




