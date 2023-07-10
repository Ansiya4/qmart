from django.contrib import admin
from coupon.models import Coupon


# Register your models here.
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('released_date','code','discount','is_expired','min_price')


