from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login_view,name='login_view'),
    path('create-account',views.create_account,name='create_account'),
    # path('signin/', views.signin, name = 'signin'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout_site, name = 'logout_site'),
    path('forgetpassword/', views.forgetpassword, name = 'forgetpassword'),
    path('resetpassword/', views.resetpassword, name = 'resetpassword'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
]
