from django.db import models
from account.models import User
from django.core.validators import MaxValueValidator

class Shop(models.Model):
    shop_name=models.CharField(max_length=60)
    gst_id=models.CharField(max_length=15, primary_key=True, unique=True)
    start_time=models.TimeField(auto_now=False, auto_now_add=False)
    stop_time = models.TimeField(auto_now=False, auto_now_add=False)
    shop_capacity=models.IntegerField()
    owner_name=models.CharField(max_length=120)
    owner_phone_number=models.CharField(max_length=10)
    shop_pincode=models.IntegerField(validators=[MaxValueValidator(999999)])
    shop_city = models.CharField(max_length=150)
    shop_area = models.CharField(max_length=500)
    shop_street = models.CharField(max_length=150)
    shop_state = models.CharField(max_length=25)
    slot_duration= models.IntegerField(default=15)
    shop_type=models.CharField(max_length=60, default='General Store')
    give_whatsapp_order=models.BooleanField(default=False)

    def to_dict(self):
        shop_dict = {
            "name": self.shop_name,
            "gst_id": self.gst_id,
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "shop_capacity": self.shop_capacity,
            "shop_owner_name": self.owner_name,
            "shop_owner_contact_number": self.owner_phone_number,
            "shop_address_pincode": self.shop_pincode,
            "shop_address_city": self.shop_city,
            "shop_address_area": self.shop_area,
            "shop_address_street": self.shop_street,
            "shop_address_state": self.shop_state
        }
        return shop_dict


class Slot(models.Model):
    shop=models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='slots')
    slot_start_time=models.DateTimeField()
    slot_stop_time=models.DateTimeField()
    num_entries_left=models.IntegerField()

    def to_dict(self):
        slot_dict={
            "owner": self.shop.to_dict(),
            "slot_start_time":self.slot_start_time,
            "slot_stop_time":self.slot_stop_time,
            "num_entries_left":self.num_entries_left
        }
        return slot_dict

    def default_entries_left(self):
        self.num_entries_left=self.shop.shop_capacity


class Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    slot=models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    shop=models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='bookings')
    is_message=models.BooleanField(default=False)
    message_for_shopkeeper=models.CharField(max_length=256, null=True)
