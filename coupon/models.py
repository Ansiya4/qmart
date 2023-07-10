from django.db import models

class Coupon(models.Model):
    
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    released_date = models.DateTimeField(auto_now_add=True,null=True)
    is_expired = models.BooleanField(default=False)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    

    