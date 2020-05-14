from account.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.auth_helpers import get_jwt_with_user



@api_view(['POST'])
def register(request):
    try:
        first_name = request.data['first_name']
        email = request.data['email']
    except KeyError:
        return Response({'error':'Either first name or email is not Provided'},status=status.HTTP_403_FORBIDDEN)

    if User.objects.filter(email=email).count() != 0:
        return Response({'error':'A User is already registered with this email id'},status=status.HTTP_403_FORBIDDEN)
    user = User(first_name=first_name,email=email)
    password = request.data['password']
    user.last_name=request.data['last_name']
    user.set_password(password)
    user.save()
    user.refresh_from_db()
    user.save()

    token = get_jwt_with_user(user)

    return Response({'token':token,'username':user.first_name,'email':user.email},status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response({'error':'Either email or password is not provided'},status=status.HTTP_403_FORBIDDEN)

    user = authenticate(request,email=email,password=password)

    if user:
        token = get_jwt_with_user(user)
        return Response({'token':token},status=status.HTTP_200_OK)
    else:
        return Response({'error':'Invalid Login details supplied.'},status=status.HTTP_403_FORBIDDEN)