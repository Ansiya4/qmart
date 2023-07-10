from django import forms
from loginSystem.models import Account
from .models import adress


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields =['first_name', 'last_name', 'username', 'phone_number']

class adressForm(forms.ModelForm):
    class Meta:
        model = adress
        fields= [ 'house','city','state','country','pin']
