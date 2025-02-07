import requests


BASE_URL='http://shop.socorsnearyou.xyz'
# BASE_URL='http://127.0.0.1:8000'


def send_buy_in_to_shopkeeper(slot_id, buyin_id, user_id, user_name):
    url = BASE_URL+'/api/create-buyin/'
    payload = {
        "slot_id": slot_id,
        "buyin_id": buyin_id,
        "user_id": user_id,
        "user_name": user_name
    }
    res = requests.post(url=url, data=payload)
    res_json = res.json()
    if res_json['status'] == False:
        return False
    else:
        return True

def send_pick_up_to_shopkeeper(is_delivery,slot_id, pickup_id, user_id, user_name, message):
    url = BASE_URL + '/api/create-pickup/'
    payload = {
        "is_delivery": is_delivery,
        "slot_id": slot_id,
        "pickup_id": pickup_id,
        "user_id": user_id,
        "user_name": user_name,
        "message":message
    }
    res = requests.post(url=url, data=payload)
    res_json = res.json()
    if res_json['status'] == False:
        return False
    else:
        return True

def create_slot(slot_id, shop_id, start_time, stop_time):
    url = BASE_URL+'/api/create-slot/'
    payload = {
        "slot_id"   : slot_id,
        "shop_id"   : shop_id,
        "start_time": start_time,
        "stop_time" : stop_time
    }
    res = requests.post(url=url, data=payload)
    res_json=res.json()
    if res_json['status']==False:
        return False
    else:
        return True


