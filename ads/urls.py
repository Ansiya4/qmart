from django.urls import path
from . import views

urlpatterns = [
    path('ad_management', views.ad_management, name='ad_management')
]   