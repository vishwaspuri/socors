from django import forms
from .models import User, Address


class AddressForm(forms.ModelForm):
    class Meta(object):
        model = Address
        fields = ['city', 'area', 'street', 'state', 'pincode']

class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(required=False)
    ph_number = forms.CharField(required=False)
    email     = forms.EmailField(required=False)

    class Meta:
        model   = User
        fields  = (
            'full_name',
            'email',
            'ph_number'
        )

