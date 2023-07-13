import decimal
from django.shortcuts import get_object_or_404, redirect, render
from loginSystem.models import Account
from coupon.models import Coupon
from order.models import UsedCoupon
from .models import Cart,CartItem
from product.models import Product
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import F,Sum
from userSystem.models import adress
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore



# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
def cart_view(request):
    user_id = request.session.get('user_id')
    print(user_id,"aaaaaaaaaaaaaaa")
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    try:
        user_cart = Cart.objects.get_or_create(user=user)
        user_cart = Cart.objects.get(user=user)
        filtered_items = CartItem.objects.filter(cart=user_cart).order_by('-cart__created_at')
    
        subtotal =  float(user_cart.get_total_price()) if  user_cart.get_total_price() else 0
        tax = float(subtotal) * 0.18
        grandtotal = subtotal + tax
        context = {
        'subtotal':subtotal,
        'tax':tax,
        'grandtotal':grandtotal,
        'cart_items': filtered_items,
        'user': user,
        'products': user
        }
        return render(request, 'user_view/mycart.html', context)

    except:
        user_cart =None
        context={
            'user': user
        }
        return render(request, 'user_view/mycart.html',context )
   

from django.contrib.auth.models import AnonymousUser

@login_required
def addTocart(request):
    product_id = request.POST['product_id']
    product = get_object_or_404(Product, pk=product_id)
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    my_item = product.product_name
    if product.is_available and product.product_qnty > 0:
        cart = Cart.objects.get_or_create(user=user)
        cart = Cart.objects.get(user=user)
        productExist = CartItem.objects.filter(cart=cart,product=product).exists()
        if not productExist:
            print('Its new product to this cart')
            CartItem.objects.create(cart=cart,product=product,price=product.price)
            messages.success(request,f"{my_item} added Successfully")
        else:
            messages.success(request,f"{my_item} already exist")
    else:
        messages.success(request,f"{my_item} is not available now")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_update(request):
    if request.POST.get('action') == 'post':
            user_id = request.session.get('user_id')
            product_id = int(request.POST.get('product_id'))
            product_quantity = int(request.POST.get('product_quantity'))
            if user_id:
                user = Account.objects.get(id=user_id)
            else:
                return JsonResponse('User not found!!',safe=False)
            cart = Cart.objects.get(user=user)
            product = get_object_or_404(Product, pk=product_id)
            item = CartItem.objects.get(cart=cart,product=product)
            new_quantity = product_quantity
            if new_quantity > product.product_qnty:
                error_message = 'Quantity exceeds available stock'
                response = JsonResponse({'error': error_message})
                return response
            else:
                item.quantity = new_quantity
                item.save()
                subtotal = float(cart.get_total_price())
                tax = float(subtotal) * 0.15
                grandtotal = subtotal + tax
                product_total = product.price * product_quantity
                response = JsonResponse({'qty':product_quantity, 'product_total':product_total,'subtotal':subtotal, 'tax':tax,'grandtotal':grandtotal})
                return response

# USER CART DELETE    
def delete_cart(request,product_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    cart = Cart.objects.get(user=user)
    product = get_object_or_404(Product, pk=product_id)
    CartItem.objects.get(cart=cart,product=product).delete()
    return redirect('cart_view')
@login_required
def checkout_cart(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
        # cart = Cart.objects.get(user=user)
    else:
        user = None
    new_coupon = None
    if request.method == 'POST':
        new_coupon=request.POST.get('coupon')
        try:
            coupon_exists=Coupon.objects.filter(code=new_coupon,is_expired = False)
        except:
            coupon_exists=None
        if coupon_exists:
            coupon_used = UsedCoupon.objects.filter(coupon_used=new_coupon,order__customer=user).exists()
            if coupon_used:
                messages.success(request,'Coupon already used')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
            else:
                if user_id:
                    cart_items = CartItem.objects.filter(cart__user_id=user_id)
                    if cart_items:
                        total = sum(item.product.price * item.quantity for item in cart_items)
                        shipping_rate = decimal.Decimal('50.00')
                        tax = decimal.Decimal(str(total)) * decimal.Decimal('0.18')
                        grand_total = total+shipping_rate+tax
                        coupon = coupon_exists.get()
                        if grand_total >= coupon.min_price:
                            new_total = grand_total-coupon.discount

                        else:
                            message = "You must purchase above " + str(coupon.min_price)
                            messages.info(request, message)
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    else:
                        messages.info(request,"Cart is Empty")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
                else:
                    cart_items = []
                    total = 0
                user_address = adress.objects.filter(user=user,is_shipping = True)
                context = {
                    'user' :user,
                    'cart' :cart_items,
                    'totalsum' :total,
                    'shipping_rate' :shipping_rate,
                    'grand_total' :grand_total,
                    'address':user_address,
                    'tax': tax,
                    'coupon':coupon_exists,
                    'new_total':new_total
                }
            return render(request, 'user_view/checkout.html', context)
        else:
            messages.success(request,'Invalid coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        
    else:
        if user_id:
            cart_items = CartItem.objects.filter(cart__user_id=user_id)
            if cart_items:
                total = sum(item.product.price * item.quantity for item in cart_items)
                shipping_rate = decimal.Decimal('50.00')
                tax = decimal.Decimal(str(total)) * decimal.Decimal('0.18')
                grand_total=total+shipping_rate+tax
            else:
                messages.info(request,"Cart is Empty")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        else:
            cart_items = []
            total = 0
        user_address = adress.objects.filter(user=user,is_shipping = True)
        context = {
            'user' :user,
            'cart' :cart_items,
            'totalsum' :total,
            'shipping_rate' :shipping_rate,
            'grand_total' :grand_total,
            'address':user_address,
            'tax': tax
        }

        return render(request, 'user_view/checkout.html', context)