from django import forms
from order.models import Order,Ordered_Product
from userSystem.models import adress

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name_of_person', 'phone_number','mode_of_payment','address','coupon']
        
    def clean(self):
        cleaned_data = super().clean()
        mode_of_payment = cleaned_data.get('mode_of_payment')
        address = cleaned_data.get('address')
        phone_number = cleaned_data.get('phone_number')

        if not mode_of_payment:
            self.add_error('mode_of_payment', "Please provide a mode of payment.")

        if not address:
            self.add_error('address', "Please provide an address.")
        
        # if phone_number:
        #     self.add_error('phone_number',"some error in phone_number")

        
        return cleaned_data