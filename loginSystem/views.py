# from typing import Self
from django.shortcuts import render,redirect

# from qmart.ads import admin
from .models import Account, UserOTP
from django.contrib import messages,auth
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import login, logout
from .backends import CustomAuthenticationBackend
from ads.models import main_ad
from order.models import Order,Ordered_Product
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import datetime,timedelta
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def dashboard(request):
    if not request.user.is_superuser:
        return redirect(home)
    delivered_items = Ordered_Product.objects.filter(status='Delivered')
    revenue = 0
    for item in delivered_items:
        revenue += item.order_id.total_amount
    top_selling = Ordered_Product.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]
    recent_sale = Ordered_Product.objects.all().order_by('-id')[:5]
    today = datetime.today()
    date_range = 7
    four_days_ago = today - timedelta(days=date_range)
    orders = Order.objects.filter(time_of_order__gte=four_days_ago, time_of_order__lte=today)
    sales_by_day = orders.annotate(day=TruncDay('time_of_order')).values('day').annotate(total_sales=Sum('total_amount')).order_by('day')
    sales_dates = Order.objects.annotate(sale_date=Cast('time_of_order', output_field=DateField())).values('sale_date').distinct()
    context = {
        'total_users':Account.objects.count(),
        'sales':Ordered_Product.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    return render(request,'dashboard_view/dashboard.html',context)

def home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    print(user)
    try:
        new_ad=main_ad.objects.first()
    except:
        new_ad=None
    context = {
        'ads':new_ad,
        'user':user
    }
    return render(request, 'user_view/home.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if email == '':
            messages.info(request,'email required')
            return redirect(login_view)
        elif password == '':
            messages.info(request,'password required')
            return redirect(login_view)
        try:
            Account.objects.get(email=email)
        except:
            messages.info(request,'No account found')
            return redirect(login_view)
        if Account.objects.get(email=email).is_blocked:
            messages.info(request,"Your account is blocked, Please try later")
            return redirect(login_view)
        if user is not None:
            if user.is_superuser:
                login(request,user)

                return redirect('dashboard')
            else:
                if user.is_active:
                    login(request,user)
                    return redirect('home')  
                else:
                     messages.info(request,"Your account is temporarily blocked, Please try later")
                     return redirect('login_view')
        else:
            messages.info(request,'credential mismatch')
            return redirect(login_view)
    else:
        user = None
        return render(request,'user_view/login.html',{'user':user})
    
def logout_site(request):
    logout(request)
    request.session.flush()
    return redirect('home')   

def create_account(request):
    return render(request,'user_view/register.html')

def validateEmail( email ):
    from django.core.validators import validate_email
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    else:
        return False
    

# Create your views here.

def register(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=Account.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                login(request,usr,backend='loginSystem.backends.CustomAuthenticationBackend')
                messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                request.session['user_id'] = usr.id
                return redirect('home')
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'user_view/register.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            firstname = request.POST['firstname'] 
            lastname = request.POST['lastname']  
            name = request.POST['name']
            email = request.POST['email']
            # phone_number = request.POST['mobile']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
             # null values checking
            check = [name,email,password1,password2]
            for values in check:
                if values == '':
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'user_view/register.html',context)
                else:
                    pass

            result = validate_name(name)
            if result is not False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,result)
                return render(request,'user_view/register.html',context)
            else:
                pass
            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'user_account/register.html',context)
            else:
                pass
                        
            Pass = ValidatePassword(password1)
            if Pass is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter Strong Password')
                return render(request,'user_view/register.html',context)
            else:
                pass
            if password1 == password2:
                try:
                    Account.objects.get(email=email)
                except:
                    usr = Account.objects.create_user(first_name=firstname, last_name=lastname, username=name,email=email,password=password1)
                    usr.is_active=False
                    usr.save()
                    
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for Beauty Mart is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to Beauty Mart Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    return render(request,'user_view/register.html',{'otp':True,'usr':usr})
                else:
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.error(request,'user already exist')
                    return render(request,'user_view/register.html',context)
            else:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.error(request,'password mismatch')
                return render(request,'user_view/register.html',context)
    else:
        return render(request,'user_view/register.html')

def forgetpassword(request):
    if request.method == 'POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=Account.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr,backend='loginSystem.backends.CustomAuthenticationBackend')
                messages.success(request,f'Now you can reset your password {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return render(request, 'user_view/resetpassword.html',{'user':usr})
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request, 'user_view/forgetpassword.html',{'otp':True,'usr':usr})
        # User rigistration validation
        else:
            email = request.POST.get('email')
            if Account.objects.filter(email=email).exists():
                usr = Account.objects.get(email__exact=email)
                user_otp=random.randint(1000,9999)
                UserOTP.objects.create(user=usr,otp=user_otp)
                mess=f'Hello\t{usr.username},\nYour OTP to forgot password is {user_otp}\nThanks!'
                send_mail(
                        "welcome to Beatandbase Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                messages.success(request, 'OTP sent to you email')
                return render(request, 'user_view/forgetpassword.html',{'otp':True,'usr':usr})

            else:
                messages.error(request, 'Account does not exist!')
                return redirect('forgot_password')
    return render(request, 'user_view/forgetpassword.html')

from django.core.exceptions import ValidationError

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
def resetpassword(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    if request.method=='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            # user = request.POST.get('fjkha67UTAnh?"}[njkGTFCXD#A@!21^^*87ghjuguy67')
            Pass = ValidatePassword(password)
            if Pass is False:
                messages.success(request, 'Enter Strong password')
                
                return redirect('resetpassword')
            if user is None:
                email = request.POST.get('email')
                try:
                    user = Account.objects.get(email=email)
                except:
                    return redirect('home')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset succesfull')
            return redirect('user_profile')
        else:
            messages.error(request, 'Password doesnot match')
            return redirect('resetpassword')

    return render(request, 'user_view/resetpassword.html')

