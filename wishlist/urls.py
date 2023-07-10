from django.urls import path
from . import views

urlpatterns = [
    
    path('add-to-wishlist/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist-deleted/',views.delete_wishlist,name='delete_wishlist'),
    
]