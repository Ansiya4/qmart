from django.shortcuts import render,redirect
from loginSystem.models import Account
from django.contrib import messages
from datetime import datetime
from order.models import Ordered_Product,Order


# Create your views here.


def sales_report(request):
    # if not request.user.is_superuser:
    #     return redirect('dashboard')
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        
        if start_date == '' or end_date == '':
            messages.error(request, 'Give date first')
            return redirect(sales_report)
        if start_date == end_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = Ordered_Product.objects.filter(order_id__created_at__date=date_obj.date(),status='Delivered')
            if order_items:
                context.update(sales=order_items, s_date=start_date, e_date=end_date)
                return render(request, 'sales.html', context)
            else:
                messages.error(request, 'No data found')
            return redirect(sales_report)

        order_items = Ordered_Product.objects.filter(order_id__time_of_order__date__gte=start_date, order_id__time_of_order__date__lte=end_date,status='Delivered')

        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date)
        else:
            messages.error(request, 'No data found')
    return render(request, 'sales.html', context)
    

def user_details(request):
    customers = Account.objects.exclude(is_superuser=True).order_by('id')
    context={
        'customer':customers
    }
    return render(request,'dashboard_view/user_manager.html',context)

def block(request,id):
    customer = Account.objects.get(id = id)
    if customer.is_active:
        customer.is_active =False
        customer.save()
    else:
        customer.is_active = True
        customer.save()
    return redirect('user_details')