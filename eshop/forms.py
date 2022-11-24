
from django import forms
from .models import UserAddress
from django.contrib.auth.models import User


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ('id','address1','address2','city','state','country','zipcode')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email')

#Paypal


