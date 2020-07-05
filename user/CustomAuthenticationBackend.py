from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
MyUser = get_user_model()

class PhNumberOrEmailBackend(ModelBackend):
    def authenticate(self, request,username=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(Q(email=username) | Q(ph_number=username))
            if user.check_password(password):
                return user
        except:
            MyUser().set_password(password)