from django.urls import path
from . import views

urlpatterns = [
   
    path('product/',views.product_page,name='product_page'),
    path('product/<slug:category_slug>/',views.product_page,name='product_by_category'),
    path('profile/',views.user_profile,name='user_profile'),
    # path('loadprofile/',views.loadprofile,name='loadprofile'),
    path('profile-edit/',views.edit_profile,name='edit_profile'),
    path('address/',views.add_address,name='add_address'),
    path('address/<int:adr_id>',views.delete_address,name='delete_address'),
    path('edit',views.edit_address,name='edit_address'),
    path('price/<slug:category_slug>/<int:min_price>/<int:max_price>/', views.price_ranges_view, name='price_ranges_view_with_category'),
    path('price/<int:min_price>/<int:max_price>/', views.price_ranges_view, name='price_ranges_view'),
    path('address-list/',views.address_manager,name='address_manager'),
    
    # path('error_404/',views.error_404,name='error_404'),
#     # path('signin/', views.signin, name = 'signin'),
#     path('register/', views.register, name = 'register'),
#     path('logout_site/', views.logout_site, name = 'logout_site'),
#     path('forgetpassword/', views.forgetpassword, name = 'forgetpassword'),
#     path('resetpassword/', views.resetpassword, name = 'resetpassword'),
#     path('dashboard/', views.dashboard, name = 'dashboard'),
]