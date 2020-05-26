#API Reference

## User APIs:

- OTP Generation on registeration:
    - POST: ```user/api/validate-phone/``` <br/>
        ```
        {
              "phone": <ph_number>,
              "full_name": <full_name>,
              "email": <email_id>,
              "password": password
        }
        ```
- OTP Verification:
    - POST: ```user/api/otp/```<br/>
    ```
        {
            "phone": <ph_number>,
            "otp": <user_otp>
        }
  ```
- Profile Details:
    - GET: ```user/api/user-details/```
- Add address for user:
    - POST: ```user/api/new-address/```<br/>
        ```
        {
            "city": city,
            "area": area,
            "street": street,
            "state": state,
            "pincode": pincode
        }
        ```
## Slot API's

- GET(Shops in same pincode)        : ```api/shop-list/<int:pincode>/```
- GET(Shop details given the gst id): ```api/shop-slots/<str:gst_id>/``` 
- POST(Book Slot): ```api/book-slot/```
    - ```
        {
            "gst_id": <shop-gst-id>,
            "slot_id": <slot_id>, 
        }
      ```
- GET(Booked slots for a given user): ```api/user-bookings/```
- GET(Shops by category): ```api/shops-by-category-and-city/<category-code>/```
           
- GET(Shop Search) ```api/shop-search/<Query>/```    
        