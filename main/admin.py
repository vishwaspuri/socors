from django.contrib import admin
from .models import Shop,Slot,PickUpBooking, BuyInBooking
# Register your models here.

admin.site.register(Shop)
admin.site.register(Slot)
admin.site.register(PickUpBooking)
admin.site.register(BuyInBooking)