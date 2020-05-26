from django import forms
from .models import User, Address


class AddressForm(forms.ModelForm):
    class Meta(object):
        model = Address
        fields = ['city', 'area', 'street', 'state', 'pincode']