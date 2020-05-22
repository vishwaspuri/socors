from user.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.auth_helpers import get_jwt_with_user
from user.otp_helper import get_otp, send_otp
from rest_framework.views import APIView
from user.models import PhoneOTP, LoginOTP

@api_view(['POST'])
def register(request):
    try:
        full_name = request.data['full_name']
        email = request.data['email']
    except KeyError:
        return Response({'error':'Either first name or email is not Provided'},status=status.HTTP_403_FORBIDDEN)

    if User.objects.filter(email=email).count() != 0:
        return Response({'error':'A User is already registered with this email id'},status=status.HTTP_403_FORBIDDEN)
    user = User(full_name=full_name,email=email)
    password = request.data['password']
    user.set_password(password)
    user.save()
    user.refresh_from_db()
    user.save()

    token = get_jwt_with_user(user)

    return Response({'token':token,'username':user.full_name,'email':user.email},status=status.HTTP_201_CREATED)

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


# -------------------------------------------------------------------------------------------
# ------------------------------OTP VIEWS----------------------------------------------------
# -------------------------------------------------------------------------------------------


class ValidatePhoneSendOTP(APIView):
    def post(self, request, *args, **kwargs):
        try:
            phone_number = request.data.get('phone')
        except:
            return Response({
                'status': False,
                'detail': 'Please send the otp and phone number correctly!'
            }, status=status.HTTP_403_FORBIDDEN)
        try:
            full_name = request.data['full_name']
            email = request.data['email']
        except KeyError:
            return Response({'error': 'Either full name or email is not Provided'}, status=status.HTTP_403_FORBIDDEN)
        try:
            password = request.data['password']
        except KeyError:
            return Response({'error': 'Either first name or email is not Provided'}, status=status.HTTP_403_FORBIDDEN)
        if User.objects.filter(email=email).count() != 0:
            return Response({'error': 'A User is already registered with this email id'},
                            status=status.HTTP_403_FORBIDDEN)

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(ph_number__iexact=phone)
            if not user.exists():
                new_user = User(full_name=full_name, email=email)
                new_user.ph_number=phone
                new_user.set_password(password)
                new_user.save()
                new_user.refresh_from_db()
                new_user.save()
                key=get_otp(phone)
                if key:
                    old=PhoneOTP.objects.filter(phone__iexact= phone)
                    if old.exists():
                        old=old.first()
                        count=old.count
                        if count>9:
                            new_user.delete()
                            return Response({
                                        'status': False,
                                        'detail': 'You have reached otp response limit. Please contact customer service!'
                                    }, status=status.HTTP_403_FORBIDDEN)
                        else:
                            send_otp(phone, 'USER', key)
                            old.otp=key
                            old.count=old.count+1
                            old.save()
                            return Response({
                                'status': True,
                                'detail': 'OTP sent successfully!'
                            }, status=status.HTTP_200_OK)
                    else:
                        otp_object = PhoneOTP.objects.create(
                            phone=phone,
                            otp=key
                        )
                        send_otp(phone, 'USER', key)
                        otp_object.save()
                        return Response({
                                'status': True,
                                'detail': 'OTP sent successfully!'
                                }, status=status.HTTP_200_OK)
                else:
                    new_user.delete()
                    return Response({
                        'status': False,
                        'detail': 'Unable to send otp try again!'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone number already exists!'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'status': False,
                'detail': 'Phone number is not given in the post request'
            }, status=status.HTTP_403_FORBIDDEN)

class validateOTP(APIView):
    def post(self, request, *args, **kwargs):
        try:
            phone    = request.data['phone']
            otp_sent = request.data['otp']
        except:
            return Response({
                'status': False,
                'detail': 'Phone number is not given in the post request'
            }, status=status.HTTP_403_FORBIDDEN)
        phone=str(phone)
        otp_sent=str(otp_sent)
        actual_otp=PhoneOTP.objects.filter(phone__iexact= phone).first()
        if (str(actual_otp.otp)==otp_sent):
            user=User.objects.filter(ph_number__iexact=phone).first()
            actual_otp.validated=True
            actual_otp.save()
            if user:
                token = get_jwt_with_user(user)
                return Response({'token': token, 'username': user.full_name, 'email': user.email},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': False,
                    'detail': 'Fill the user form first!'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'status': False,
                'detail': 'Incorrect otp!'
            }, status=status.HTTP_403_FORBIDDEN)



class GenerateOTPforLogin(APIView):
    def post(self,request, *args, **kwargs):
        try:
            email = request.data['email']
        except:
            return Response({
                'status': False,
                'detail': 'Phone number not sent!'
            }, status=status.HTTP_403_FORBIDDEN)
        user=User.objects.filter(email= email).first()
        if not user.exists():
            return Response({
                'status': False,
                'detail': 'The user requested does not exist!'
            }, status=status.HTTP_403_FORBIDDEN)
        key=get_otp(user.ph_number)
        if key:
            old_otp=LoginOTP.objects.filter(phone__iexact=user.ph_number)
            if old_otp.exists():
                count=old_otp.count
                if count>100:
                    return Response({
                        'status': False,
                        'detail': 'You have reached otp response limit. Please contact customer service!'
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
                    old_otp.otp=key
                    send_otp(user.ph_number, 'USER', key)
                    old_otp.count=old_otp.count+1
                    old_otp.save()
                    return Response({
                        'status': False,
                        'detail': 'OTP sent!'
                    }, status=status.HTTP_200_OK)
            else:
                otp_obj = LoginOTP()
                otp_obj.otp=key
                send_otp(user.ph_number, 'USER', key)
                otp_obj.count=1
                otp_obj.phone=user.ph_number
                otp_obj.save()
                return Response({
                    'status': False,
                    'detail': 'OTP sent!'
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'detail': 'Unable to send otp try again!'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AuthenticateLoginOTP(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email=request.data['email']
        except:
            return Response({
                'status': False,
                'detail': 'Please send phone number!'
            }, status=status.HTTP_403_FORBIDDEN)
        try:
            otp=request.data['otp']
        except:
            return Response({
                'status': False,
                'detail': 'Please send OTP!'
            }, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.filter(email=email).first()
        if not user.exists():
            return Response({
                'status': False,
                'detail': 'The user requested does not exist!'
            }, status=status.HTTP_403_FORBIDDEN)
        actual_otp=LoginOTP.objects.filter(phone__iexact=user.ph_number)
        if actual_otp.exists():
            if str(actual_otp.otp)==str(otp):
                pass
            else:
                return Response({
                    'status': False,
                    'detail': 'Incorrect otp!'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'status': False,
                'detail': 'Generate OTP first!'
            }, status=status.HTTP_403_FORBIDDEN)