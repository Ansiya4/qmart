from django.db import models
from loginSystem.models import Account
from product.models import Product
# Create your models here.
class Wishlist(models.Model):
    customer =  models.ForeignKey(Account, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)