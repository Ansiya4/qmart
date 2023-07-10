from django.urls import path
from . import views

urlpatterns = [
    
    path('place_order/',views.place_order,name='place_order'),
    path('view_order/',views.view_order,name='view_order'),
    path('order_management/',views.order_management,name='order_management'),
    path('order_details/<int:order_id>',views.order_details,name='order_details'),
    path('change_status/',views.change_status,name='change_status'),
    path('cancel_order/<int:cancel_id>',views.cancel_order,name='cancel_order'),
    path('remove_order/<int:cancel_id>',views.remove_order,name='remove_order'),
    path('proceed-to-pay/',views.razerpaycheck),
    path('success/',views.success)

] 
