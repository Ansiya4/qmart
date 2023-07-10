from django.urls import path
from . import views


urlpatterns = [
    path('coupon/',views.add_coupon,name='add_coupon'),
    path('management/',views.coupon_management,name='coupon_management'),
    path('couponapplied/<>',views.apply_coupon,name='apply_coupon'),
    
] 
