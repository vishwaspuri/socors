from __future__ import absolute_import
from socors_backend.celery import app
from .models import Shop, Slot
from datetime import timedelta,datetime, date
from main.shopkeeper_helpers import create_slot
from .task_utils import closed_shop_with_no_slots



@app.task
def create_slots_for_the_day():
    shops = Shop.objects.all()
    for shop in shops:
        slot_duration = shop.slot_duration
        shop_start_time = shop.start_time
        shop_stop_time = shop.stop_time
        num_working_hrs=datetime.combine(date.today(), shop_stop_time) - datetime.combine(date.today(), shop_start_time)
        num_slots_required = int(num_working_hrs.total_seconds()/(60*slot_duration))
        st = shop_start_time
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
            create_slot(slot.slot_id, shop.gst_id,slot.slot_start_time, slot.slot_stop_time)

@app.task
def create_next_day_slots():
    shops = Shop.objects.all()
    for shop in shops:
        slot_duration = shop.slot_duration
        shop_start_time = shop.start_time
        shop_stop_time = shop.stop_time
        Date = (datetime.today() + timedelta(hours=24)).date()
        num_working_hrs = datetime.combine(Date, shop_stop_time) - datetime.combine(Date,shop_start_time)
        num_slots_required = int(num_working_hrs.total_seconds() / (60 * slot_duration))
        st = shop_start_time
        for i in range(0, num_slots_required):
            slot = Slot()
            slot.shop = shop
            slot_start = datetime.combine(Date, st)
            slot_stop = slot_start + timedelta(minutes=slot_duration)
            slot.slot_start_time = slot_start
            slot.slot_stop_time = slot_stop
            slot.default_entries_left()
            slot.save()
            st = slot_stop.time()
            create_slot(slot.slot_id, shop.gst_id, slot.slot_start_time, slot.slot_stop_time)

@app.task
def create_slots():
    shops = create_slots_for_the_day()
    for shop in shops:
        slot_duration = shop.slot_duration
        shop_start_time = shop.start_time
        shop_stop_time = shop.stop_time
        num_working_hrs=datetime.combine(date.today(), shop_stop_time) - datetime.combine(date.today()+timedelta(hours=24), shop_start_time)
        num_slots_required = int(num_working_hrs.total_seconds()/(60*slot_duration))
        st = shop_start_time
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
            create_slot(slot.slot_id, shop.gst_id,slot.slot_start_time, slot.slot_stop_time)

@app.task
def hello_world():
    print('Hello World!')