#API Reference

## User APIs:

- OTP Generation on registeration:
    - POST: ```user/api/validate-phone/``` <br/>
        {<br/>
              "phone": <ph_number>,<br/>
              "full_name": <full_name>,<br/>
              "email": <email_id>,<br/>
              "password": password<br/>
        }
- OTP Verification:
    - POST: ```user/api/otp```<br/>
    {<br/>
    "phone": <ph_number>,<br/>
    "otp": <user_otp><br/>
    }
- Profile Details:
    - GET: ```user/api/user-details/```
- Add address for user:
    - POST: ```user/api/new-address/```<br/>
    {<br/>
    "city": city,<br/>
    "area": area,<br/>
    "street": street,<br/>
    "state": state<br/>
    "pincode": pincode<br/>
    }
    
## Slot API's

- GET(Shops in same pincode)        : ```api/shop-list/<int:pincode>```
- GET(Shop details given the gst id): ```api/shop-slots/<str:gst_id>``` 
- POST(Book Slot): ```api/book-slot```
    - {<br/>
      "gst_id": <shop-gst-id>,<br/>
      "slot_id": <slot_id>, <br/>
      }
- GET(Booked slots for a given user): ```api/user-bookings```            
    
        