# from django import forms
# from .models import Product, ColorVariation


# class AddProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'category', 'description', 'price', 'product_qnty', 'image', 'is_available', 'color_name']
#         widgets = {
#                 'color_name': forms.SelectMultiple(attrs={'class': 'form-select'})
#             }