from django import forms
from loginSystem.models import Account
from .models import adress


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields =['first_name', 'last_name', 'username', 'phone_number','user_image']
    # def clean(self):
    #     cleaned_data = super().clean()

    #     # Check if last_name and first_name are empty
    #     if not cleaned_data['last_name'] and not cleaned_data['first_name']:
    #     # Get the previous data from the database
    #         last_name = self.instance.last_name
    #         first_name = self.instance.first_name

    #         # Set the data in the form
    #         cleaned_data['last_name'] = last_name
    #         cleaned_data['first_name'] = first_name

    #     return cleaned_data

class adressForm(forms.ModelForm):
    class Meta:
        model = adress
        fields= [ 'house','city','state','country','pin']
