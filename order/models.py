from django.db import models
from loginSystem.models import Account
from product.models import Product
from userSystem.models import adress
from coupon.models import Coupon

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    name_of_person = models.CharField(max_length=50,blank=True, null=True)
    phone_number = models.CharField(max_length=50,blank=False,null=True)
    address = models.ForeignKey(adress,on_delete=models.CASCADE,blank=True, null=True)
    total_amount = models.DecimalField(max_digits=50, decimal_places=2) 
    tax= models.DecimalField(max_digits=10,decimal_places=2)
    mode_of_payment = models.CharField(max_length=50,blank=True, null=False)
    time_of_order = models.DateTimeField(auto_now_add=True,null=True)
    expected_time = models.DateTimeField(null=True)
    coupon =models.ForeignKey(Coupon,on_delete=models.CASCADE,blank=True, null=True)
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    status = models.CharField(choices=STATUS,default='Order Confirmed', null=True)

class Ordered_Product(models.Model):
    order_id =  models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product  =  models.ForeignKey(Product,on_delete=models.CASCADE,blank=True, null=True )
    quantity = models.BigIntegerField()
    amount   = models.DecimalField(max_digits=20, decimal_places=2)
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    status = models.CharField(choices=STATUS,default='Order Confirmed',null=True)

class UsedCoupon(models.Model):
    coupon_used= models.CharField(max_length=50,null=True)
    order =  models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    