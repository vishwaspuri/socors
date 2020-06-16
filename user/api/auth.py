from user.models import User
from user.otp_helper import get_otp, send_otp
from user.models import PhoneOTP
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserLoginSerializer




class LoginView(APIView):
    """
    View for login a user to your system.
    **Example requests**:
        POST /api/auth/login/
    """

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        authenticated_user = authenticate(email=email, password=password)
        if authenticated_user:
            serializer = UserLoginSerializer(authenticated_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)

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
            return Response({'detail': 'Either full name or email is not Provided'}, status=status.HTTP_403_FORBIDDEN)
        try:
            password = request.data['password']
        except KeyError:
            return Response({'detail': 'Either first name or email is not Provided'}, status=status.HTTP_403_FORBIDDEN)
        if User.objects.filter(email=email).count() != 0:
            return Response({'detail': 'A User is already registered with this email id'},
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
                return Response({
                    'status': True,
                    'msg': 'redirect to login',
                    'username': user.full_name,
                    'email': user.email},status=status.HTTP_201_CREATED)
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


