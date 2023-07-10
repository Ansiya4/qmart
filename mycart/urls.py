from django.urls import path
from . import views

urlpatterns = [
    
    path('add-to-cart/',views.addTocart,name='addTocart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart-update/',views.cart_update,name='cart_update'),
    path('delete-cart/<int:product_id>',views.delete_cart,name='delete_cart'),
    path('checkout/',views.checkout_cart,name='checkout_cart'),
]  