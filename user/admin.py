from django.contrib import admin
from .models import User,Address, PhoneOTP
# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(PhoneOTP)