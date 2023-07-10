from django.urls import path
from . import views


urlpatterns = [
    
    path('user-details/',views.user_details,name='user_details'),
    path('block/<int:id>',views.block,name='block'),
    path('sales/',views.sales_report,name='sales_report'),
    
]    
    