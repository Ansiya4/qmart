from django.db import models
from loginSystem.models import Account
# Create your models here.

class adress(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,default=None)
    house= models.CharField(max_length=50,default='house')
    city = models.CharField(max_length=50,default='city')
    pin = models.CharField(max_length=50,default='pin')
    state= models.CharField(max_length=50,default='state')
    country = models.CharField(max_length=50,default='country')
    is_active = models.BooleanField(default=False)
    is_shipping= models.BooleanField(default=False)
   


class PriceRange(models.Model):
    min_price = models.IntegerField()
    max_price = models.IntegerField(null=True, blank=True)
    range_label = models.CharField(max_length=50)
        # default_ranges = [
    #    ('100-200', 100, 200),
    #    ('200-300', 200, 300),
    #    ('300-400', 300, 400),
    #    ('500-1000', 500, 1000),
    # ]
    # # Create default price range instances if they don't exist
    # for label, min_price, max_price in default_ranges:
    #     PriceRange.objects.get_or_create(range_label=label, min_price=min_price, max_price=max_price)
    def __str__(self):
        return f"{self.min_price} - {self.max_price or '+'}"



   