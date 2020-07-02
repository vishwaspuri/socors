import requests
import random

def send_otp(ph_number, user_full_name, otp):
    link=f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=592ac50a-bc6d-11ea-9fa5-0200cd936042&to={ph_number}&from=SOCORS&templatename=scocorsAuthentication&var1={user_full_name}&var2={otp}'
    req_data=requests.get(link)
    print(req_data)


def get_otp(phone):
    if phone:
        key=random.randint(999, 9999)
        return key
    else:
        return False

