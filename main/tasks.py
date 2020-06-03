# from __future__ import absolute_import
# from socors_backend.celery import app
from .models import Shop, Slot
from datetime import timedelta,datetime, date
import uuid


def create_slots_for_the_day():
    shops = Shop.objects.all()
    today = date.today()
    for shop in shops:
        slot_duration = shop.slot_duration
        shop_start_time = shop.start_time
        shop_stop_time = shop.stop_time
        num_working_hrs=datetime.combine(date.today(), shop_stop_time) - datetime.combine(date.today(), shop_start_time)
        num_slots_required = int(num_working_hrs.total_seconds()/(60*slot_duration))
        print(num_slots_required)
        st = shop_stop_time
        for i in range(0, num_slots_required):
            slot = Slot()
            slot.shop = shop
            slot_start = datetime.combine(date.today(), st)
            slot_stop = slot_start+timedelta(minutes=slot_duration)
            slot.slot_start_time = slot_start
            slot.slot_stop_time = slot_stop
            slot.default_entries_left()
            slot.save()
            st = slot_stop.time()