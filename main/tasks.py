from __future__ import absolute_import
from socors_backend.celery import app
from .models import Shop, Slot
from datetime import timedelta,datetime



@app.task
def hello_world():
    print('hello_world')



@app.task
def add_slots():
    shops=Shop.objects.all()
    for shop in shops:
        last_slot=shop.slots.all().order_by('-slot_start_time').first()
        if last_slot!=None:
            new_slot=Slot()
            new_slot.shop=shop
            new_slot.slot_start_time=last_slot.slot_stop_time
            duration=int(shop.slot_duration)
            new_slot.slot_stop_time=new_slot.slot_start_time+timedelta(minutes=duration)
            new_slot.default_entries_left()
            new_slot.save()
        else:
            new_slot=Slot()
            new_slot.shop = shop
            new_slot.slot_start_time=datetime.now()
            duration = int(shop.slot_duration)
            new_slot.slot_stop_time = new_slot.slot_start_time + timedelta(minutes=duration)
            new_slot.default_entries_left()
            new_slot.save()