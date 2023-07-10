from django.shortcuts import get_object_or_404, redirect, render
from category.models import Category
from product.models import Product
from loginSystem.models import Account
from django.core.exceptions import ObjectDoesNotExist
from .models import adress
from .forms import AccountForm,adressForm
from django.contrib import messages
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from .models import PriceRange
from django.db.models import Q
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

def price_ranges_view( request, category_slug = None, min_price=None, max_price = None):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    price_ranges = PriceRange.objects.all()
    categories = None
    products_list = None
    if category_slug != None:
        categories = Category.objects.get(slug=category_slug)
        products_list = Product.objects.filter(category = categories,price__range=(min_price, max_price))
    else:
        products_list = Product.objects.filter(price__range=(min_price, max_price))
    context = {
        'products_list' : products_list,
        'user': user,
        'price': price_ranges, 
        'category':categories,
    }
    return render(request, 'user_view/product.html', context)

# USER PRODUCT VIEW BY CATEGORY
def product_page(request, category_slug = None):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    default_ranges = [
       ('100-200', 100, 200),
       ('200-400', 200, 400),
       ('400-600', 400, 600),
       ('600-800', 600, 800),
       ('800+', 800, 0),
    ]
    # Create default price range instances if they don't exist
    for label, min_price, max_price in default_ranges:
        PriceRange.objects.get_or_create(range_label=label, min_price=min_price, max_price=max_price)
    price_ranges = PriceRange.objects.all()
    categories = None
    products_list = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products_list = Product.objects.filter(category = categories)
    else:
        products_list = Product.objects.order_by('product_name').distinct('product_name')
    context = {
        'products_list' : products_list,
        'user': user,
        'price': price_ranges, 
        'category':categories,
    }
    return render(request,'user_view/product.html',context)

def user_profile(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    # print(user)
    try:
        user_address = adress.objects.filter(user=user,is_active=True)
    except:
        user_address = None   
    context = {
        'user': user,
        'address':user_address,
    }
    return render(request,'user_view/profile.html',context)


# USER EDIT PROFILE
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        account_form = AccountForm(request.POST, instance=user)
        if account_form.is_valid():
            account_form.save()
            return redirect('user_profile')
    context={
        'user': user,
    }
    return render(request,'user_view/edit_profile.html',context)

def add_address(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    my_address = None
    try:
        my_address =adress.objects.get(user=user,is_active=True)
    except ObjectDoesNotExist:
         my_address= None
    if request.method == 'POST':
        if my_address is None:
            my_address=adress(user = user, is_active = True,is_shipping=True)
            address_form = adressForm(request.POST, instance=my_address)
            # print("acount form >>>>>>>>>>>>",address_form.is_valid())
            # print("acount form >>>>>>>>>>>>",address_form.errors)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user =user
                address_form.save()
                messages.success(request, 'Address added successfully')
                # return redirect('user_profile')
        else:
            my_address=adress(user = user, is_active = False, is_shipping = True)
            address_form = adressForm(request.POST, instance=my_address)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user =user
                address_form.save()
                messages.success(request, 'Address added successfully')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# USER MY ADDRESS
def address_manager(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    try: 
        my_address =adress.objects.filter(user=user)
    except:
        my_address=None
    context={
        'user': user,
        'address': my_address
    }
    return render(request,'address.html',context)

# USER DELETE ADDRESS
def delete_address(request,adr_id):
    my_address =adress.objects.filter(id=adr_id)
    my_address.delete()
    return redirect('address_manager')

# USER EDIT ADDRESS
def edit_address(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    my_address = None
    if request.method == 'POST':
        address_id = request.POST.get('id')
        print(address_id,"..................adress_id")
        try:
            my_address =adress.objects.get(id = address_id)
        except ObjectDoesNotExist:
            my_address= None
        print(my_address,"..................adress_id")
   
        if my_address:
            address_form = adressForm(request.POST, instance=my_address)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user =user
                address_form.save()
                messages.success(request, 'Address added successfully')
            else:
                for field, errors in address_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    return redirect('address_manager')

def error_404(request, exception):
    return render(request, '404.html', status=404)














# USER PROFILE VIEW
# def loadprofile(request):
#     user_id = request.session.get('user_id')
#     print(user_id,"aaaaaaaaaaaaaaa")
#     if user_id:
#         user = Account.objects.get(id=user_id)
#     else:
#         user = None
#     print(user)
#     try:
#         my_address = myAdress.objects.get(user=user)
#         my_address_id = my_address.id
#         user_address = adress.objects.filter(myadress=my_address_id)
#     except ObjectDoesNotExist:
#         user_address = None

#     print(user_address,"qqqqqqqqqqqqqqqqqqqqqqqqq")
    
#     context = {
#         'user': user,
#         'address':user_address,
#     }
    
#     return redirect('loadprofile',context)
