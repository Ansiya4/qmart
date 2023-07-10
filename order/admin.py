from django.contrib import admin
from .models import Order,Ordered_Product,UsedCoupon
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer' , 'name_of_person','phone_number','address','total_amount','tax','mode_of_payment','time_of_order','status')
   

@admin.register(Ordered_Product)
class Ordered_ProductAdmin(admin.ModelAdmin):
    list_display =('order_id','product','quantity','amount','status')


@admin.register(UsedCoupon)
class UsedCoupon(admin.ModelAdmin):
    list_display = ('coupon_used','order')