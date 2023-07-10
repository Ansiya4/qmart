from django.urls import path
from . import views


urlpatterns = [
    
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category_manager/',views.category_manager,name='category_manager'),
]    
    
    # path('product_page/<slug:category_slug>/',views.product_page,name='product_by_category'),
    # path('product_page/search',views.search,name='search'),
   

