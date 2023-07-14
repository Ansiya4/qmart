from django.urls import path
from . import views

urlpatterns = [
    path('add-product/',views.add_product,name='add_product'),
    path('edit-product/<int:product_id>',views.edit_product,name='edit_product'),
    path('display-product/',views.display_product,name='display_product'),
    path('delete/<int:product_id>',views.delete,name='delete'),
    path('product/search',views.search,name='search'),
    path('product-details/<int:product_id>',views.product_details,name='product_details'),
    path('product-colors/<int:product_id>/<str:color_name>/',views.product_colors,name='product_colors'),
    path('add-color/',views.add_color,name='add_color'),
    # path('category_manager/',views.category_manager,name='category_manager'),
]    
    
    
    
   

