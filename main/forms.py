from django import forms
from user.models import User, Address
from .models import PickUpBooking

class PickUpForm(forms.ModelForm):
    class Meta(object):
        model = PickUpBooking
        fields = ['message_for_shopkeeper']