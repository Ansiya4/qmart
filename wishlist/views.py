from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product
from .models import Wishlist
from django.contrib import messages
from loginSystem.models import Account


# Create your views here.
def add_to_wishlist(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    prod_id = request.POST['product_id']
    product_check = get_object_or_404(Product, pk=prod_id)
    my_item = product_check.product_name
    productExist = Wishlist.objects.filter(customer = user, product = product_check).exists()
    if request.method == 'POST':
        if user:
            if(product_check):
                if productExist:
                    messages.success(request,f"{my_item} already in wishlist")
                else:
                    Wishlist.objects.create(customer=user, product = product_check)
                    messages.success(request,f"{my_item} added to wishlist")
            else:
                messages.success(request,"No such product")
        else:
            messages.success(request,"Login to continue")
    else:
        messages.success(request,"Error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

def wishlist(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    wishlist=Wishlist.objects.all()
    context={
        'user':user,
        'wishlist':wishlist,
    }
    return render(request,'wishlist.html',context)

def delete_wishlist(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    prod_id = request.POST['product_id']
    product_check = get_object_or_404(Product, pk=prod_id)
    wishlist_item = Wishlist.objects.filter(customer=user, product=product_check)
    if wishlist_item:
        wishlist_item.delete()
    return redirect('wishlist')