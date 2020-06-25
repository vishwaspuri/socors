from .models import Shop, Slot, BreakDay
import datetime
from datetime import timedelta



# Function to return a list of shops which satisfy the following constraints:
# 1. Shops which are closed at the time function runs
# 2. Closed shops whose slots for the next day have not yet been made
# 3. The next day is not a break day
def closed_shop_with_no_slots():
    # Define dates and time
    right_now = datetime.datetime.now()
    time_now = right_now.time()
    tomorrow = right_now + timedelta(hours=24)
    tomorrow = tomorrow.date()
    # Check the shops which are closed
    # Check if the shops have next day off
    shops = Shop.objects.filter(stop_time__lte=time_now)
    shop_arr = []
    for shop in shops:
        # print(shop.shop_name)
        if  not BreakDay.objects.filter(    shop= shop, day=tomorrow).exists():
            if  not shop.are_next_day_slots_created():
                shop_arr.append(shop)
    # Return the shops that satisfy the constraints-
    return shop_arr