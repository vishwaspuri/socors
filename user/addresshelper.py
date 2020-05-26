from .models import Address,User

def make_prior_address_not_main(user_id):
    user     =User.objects.get(id=user_id)
    addresses=user.address.all()
    if addresses.exists():
        for add in addresses:
            add.is_main=False
            add.save()

