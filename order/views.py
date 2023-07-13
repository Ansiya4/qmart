import decimal
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from loginSystem.models import Account
from .models import Order, Ordered_Product
from mycart.models import Cart,CartItem
from userSystem.models import adress
from .forms import OrderForm
from django.utils import timezone
from datetime import timedelta
from order.models import Order,UsedCoupon
from django.http.response import JsonResponse
from django.db.models import F
from django.db.models import Max
from coupon.models import Coupon
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
# Create your views here.
def razerpaycheck(request):
    user_id = request.session.get('user_id')
    coupon_id = request.GET.get('coupon_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    user_cart = Cart.objects.get_or_create(user=user)
    user_cart = Cart.objects.get(user=user)
    filtered_items = CartItem.objects.filter(cart=user_cart).order_by('-cart__created_at')
    subtotal =  user_cart.get_total_price() if  user_cart.get_total_price() else 0
    tax = decimal.Decimal(str(subtotal)) * decimal.Decimal('0.18')
    tax = tax.quantize(decimal.Decimal('0.00'))
    shipping_rate = decimal.Decimal('50.00')
    total_price = subtotal + tax + shipping_rate
    if coupon_id:
        coupon = Coupon.objects.get(id=coupon_id)
        total_price = total_price - coupon.discount

    return JsonResponse({
        'total_price': total_price
    })

def success(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        phone_number = request.POST.get('phone_number')
        name_of_person = request.POST.get('name_of_person')
        address_id = request.POST.get('address_id')
        coupon_id = request.POST.get('coupon_id')
        if user_id:
            user = Account.objects.get(id=user_id)
        else:
            user = None
        user_cart = Cart.objects.get_or_create(user=user)
        user_cart = Cart.objects.get(user=user)
        filtered_items = CartItem.objects.filter(cart=user_cart).order_by('-cart__created_at')
        subtotal =  user_cart.get_total_price() if  user_cart.get_total_price() else 0
        tax = decimal.Decimal(str(subtotal)) * decimal.Decimal('0.18')
        tax = tax.quantize(decimal.Decimal('0.00'))
        shipping_rate = decimal.Decimal('50.00')
        grandtotal = subtotal + tax + shipping_rate
        time_of_order = timezone.now()
        expected_time = time_of_order + timedelta(days=14)
        payment_method = request.POST.get('mode_of_payment')
        address_instance = adress.objects.get(id=address_id)
        myorder=Order(customer=user, 
                      total_amount=grandtotal, 
                      tax=tax, 
                      time_of_order=time_of_order,
                      expected_time=expected_time, 
                      status = 'Order Confirmed',
                      mode_of_payment=payment_method,
                      name_of_person=name_of_person,
                      phone_number=phone_number,
                      address=address_instance,
                      )
        if coupon_id:
            applied_coupon = Coupon.objects.get(id=coupon_id)
            myorder.coupon = applied_coupon
        myorder.save()
        for item in filtered_items:
            if item.quantity > item.product.product_qnty:
                messages.error(request, f"Insufficient quantity available for product: {item.product.product_name}")
                return redirect('checkout_cart')
            Ordered_Product.objects.create(
                order_id=myorder,
                product=item.product,
                quantity=item.quantity,
                amount=item.get_subtotal(),
                status='Order Confirmed'
            )
            item.product.product_qnty = F('product_qnty') - item.quantity
            item.product.save()
            item.delete()
        user_cart.delete()
        if myorder.coupon:
            UsedCoupon.objects.create(coupon_used=myorder.coupon.code, order=myorder)
        return JsonResponse({'mess':'Success'})
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    max_order_id = Ordered_Product.objects.filter(order_id__customer=user,status='Order Confirmed').aggregate(Max('order_id'))['order_id__max']
    my_products= Ordered_Product.objects.filter(order_id__customer=user,order_id=max_order_id,status='Order Confirmed')
    my_order = Order.objects.get(id=max_order_id)
    new_total = my_order.total_amount
    if my_order.coupon:
        UsedCoupon.objects.create(coupon_used=my_order.coupon.code, order=my_order)
        new_total=my_order.total_amount - my_order.coupon.discount
    context = {
        'user': user,
        'myoder': my_order,
        'my_products':my_products,
        'shipping_rate':decimal.Decimal('50.00'),
        'new_total':new_total
    } 
    return render(request,'order.html',context)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    user_cart = Cart.objects.get_or_create(user=user)
    user_cart = Cart.objects.get(user=user)
    filtered_items = CartItem.objects.filter(cart=user_cart).order_by('-cart__created_at')
    subtotal =  user_cart.get_total_price() if  user_cart.get_total_price() else 0
    tax = decimal.Decimal(str(subtotal)) * decimal.Decimal('0.18')
    tax = tax.quantize(decimal.Decimal('0.00'))
    shipping_rate = decimal.Decimal('50.00')
    grandtotal = subtotal + tax + shipping_rate
    time_of_order = timezone.now()
    expected_time = time_of_order + timedelta(days=14)
    myorder = None
    if request.method == 'POST':
        myorder=Order(customer=user, total_amount=grandtotal, tax=tax, time_of_order=time_of_order,expected_time=expected_time, status = 'Order Confirmed')
        formorder=OrderForm(request.POST,instance=myorder)
        if formorder.is_valid():
            formorder.instance=myorder
            formorder.save()
            for item in filtered_items:
                if item.quantity > item.product.product_qnty:
                    messages.error(request, f"Insufficient quantity available for product: {item.product.product_name}")
                    return redirect('checkout_cart')
                Ordered_Product.objects.create(
                    order_id=myorder,
                    product=item.product,
                    quantity=item.quantity,
                    amount=item.get_subtotal(),
                    status='Order Confirmed'
                )
                item.product.product_qnty = F('product_qnty') - item.quantity
                item.product.save()
                item.delete()
            user_cart.delete()
            max_order_id = Ordered_Product.objects.filter(order_id__customer=user,status='Order Confirmed').aggregate(Max('order_id'))['order_id__max']
            my_products= Ordered_Product.objects.filter(order_id__customer=user,order_id=max_order_id,status='Order Confirmed')
            new_total = grandtotal
            if myorder.coupon:
                UsedCoupon.objects.create(coupon_used=myorder.coupon.code, order=myorder)
                new_total=myorder.total_amount - myorder.coupon.discount
            context={
            'user': user,
            'myoder':myorder,
            'my_products':my_products,
            'shipping_rate':shipping_rate,
            'new_total':new_total
            }
            messages.success(request,'form submitted successfully')
            return render(request,'order.html',context)
        else:
            for field, errors in formorder.errors.items():
                for error in errors:
                    messages.error(request, f'{formorder.fields[field].label}: {error}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

#USER VIEW ORDER
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_order(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    # active_address = adress.objects.filter(customer=user)
    view_order=Order.objects.filter(customer=user)
    order_ids = [order.id for order in view_order]
    my_order = Ordered_Product.objects.filter(order_id__in=order_ids)
    context = {
        'user': user,
        'order': view_order,
        'my_order': my_order,
    }
    return render(request,'myorder.html',context)

def cancel_order(request,cancel_id):
    my_order = Ordered_Product.objects.get(id=cancel_id)
    product = my_order.product
    quantity = my_order.quantity
    product.product_qnty += quantity
    product.save()
    my_order.status='Cancelled'
    my_order.save()
    return redirect('view_order')

def remove_order(request,cancel_id):
    my_order = Ordered_Product.objects.get(id=cancel_id)
    my_order.delete()
    return redirect('view_order')

# ADMIN ORDER MANAGEMENT
def order_management(request):
    Order_list= Order.objects.all()
    context={
        'Order_list':Order_list
    }
    return render(request,'admin_listorders.html',context)
#ADMIN VIEW ORDER DETAILS
def order_details(request,order_id):
    list_order= Ordered_Product.objects.filter(order_id = order_id)
    context={
        'order_list':list_order,
    }
    return render(request,'admin_orderdetails.html',context)

def change_status(request):
    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('order_status')
    if order_status.strip() =='':
        pass
    else:
        order_item = Ordered_Product.objects.get(id=orderitem_id)
        order_item.status = order_status
        order_item.save()
    return JsonResponse({'status': "Updated " + str(order_status) + " successfully",'order_status':order_status,})

