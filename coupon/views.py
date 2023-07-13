from django.shortcuts import redirect, render
from coupon.models import Coupon
from coupon.forms import CouponForm
from django.utils import timezone
import decimal
from django.shortcuts import get_object_or_404, redirect, render
from loginSystem.models import Account
from mycart.models import Cart,CartItem
from product.models import Product
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import F,Sum
from userSystem.models import adress
from django.contrib import messages
from order.models import UsedCoupon
from django.urls import reverse
# Create your views here.

def add_coupon(request):
    if request.method == 'POST':
        released_date = timezone.now()
        couponform = CouponForm(request.POST)
        if couponform.is_valid():
            coupon = couponform.save(commit=False)
            coupon.released_date = released_date
            coupon.save()
            return redirect('coupon_management')
        else:
            for field, errors in couponform.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        couponform = CouponForm()
    return redirect('coupon_management')


def edit_coupon(request, coupon_id):
    try:
        coupon =Coupon.objects.get(id=coupon_id)
    except:
        coupon=None
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupon_management')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'edit_coupon.html', {'form': form, 'coupon': coupon})

def coupon_management(request):
    list_coupon = Coupon.objects.all()
    context = {
        'coupon': list_coupon
    }
    return render(request,'coupon-management.html',context)

def apply_coupon(request,coupon=None):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    new_coupon = None
    if request.method == 'POST':
        new_coupon=request.POST.get('coupon')
        print(new_coupon,"new coupon...........................new coupon")
        try:
            coupon_exists=Coupon.objects.filter(code=new_coupon,is_expired = False)
        except:
            coupon_exists=None
        if coupon_exists:
            coupon_used = UsedCoupon.objects.filter(coupon_used=new_coupon,order__customer=user).exists()
            print(new_coupon,"new coupon...........................new coupon")
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
                user_address = adress.objects.filter(user=user)
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
            return render(request, 'checkout-coupon.html', context)
        else:
            messages.success(request,'Invalid coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        messages.success(request,'errorrrrrrrrrrrrrr.............')
        return redirect('checkout_cart')
