from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404,redirect
from product.models import Product,ColorVariation
from category.models import Category
from django.db.models import Q
from loginSystem.models import Account
from django.contrib import messages


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword'] 
        products_list = None
        if keyword:
            products_list= Product.objects.order_by('created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
    context ={
        'products_list': products_list, 
    }
    return render(request,'user_view/product.html',context)

# USER PRODUCT VIEW
def product_details(request,product_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_page')
    mycolors= ColorVariation.objects.all()
    same_name_products = Product.objects.filter(product_name=product.product_name)
    mycolors = ColorVariation.objects.filter(product__in=same_name_products)
    print(mycolors,"this color")
    context ={
        'product': product,
        'user':user,
        'color': mycolors,
        }
    return render(request,'user_view/single_product.html',context)

# USER PRODUCT VIEW DIFFERENT COLORS
def product_colors(request,product_id,color_name):
    user_id = request.session.get('user_id')
    if user_id:
        user = Account.objects.get(id=user_id)
    else:
        user = None
    pro_name = get_object_or_404(Product, pk=product_id)
    mycolors= ColorVariation.objects.all()
    same_name_products = Product.objects.filter(product_name=pro_name.product_name)
    mycolors = ColorVariation.objects.filter(product__in=same_name_products)
    products = Product.objects.filter(product_name=pro_name.product_name, color_name__color_name=color_name)
    product=products.first()
    context ={
        'product': product,
        'user':user,
        'color': mycolors,
        }
    return render(request,'user_view/single_product.html',context)

# ADMIN PRODUCT TABLE VIEW 
def display_product(request):
    colors= ColorVariation.objects.all()
    categ = Category.objects.all()
    prod = Product.objects.all().order_by('id')
    context = {
        'products' : prod, 
        'category' : categ, 
        'color': colors,
    }
    return render(request,'dashboard_view/product_manager.html',context)

# ADMIN DELETE A PRODUCT
def delete(request,product_id):
    prod = Product.objects.get(id=product_id)
    prod.delete()
    return redirect('display_product')

# ADMIN ADD A PRODUCT
def add_product(request):
    if request.method == "POST":
        try:
            product_name= request.POST.get('brand_name')
            category_id= request.POST.get('category')
            category = get_object_or_404(Category, id=category_id)
            description=request.POST.get('description')
            price = request.POST.get('price')
            product_qnty = request.POST.get('product_qnty')
            image=request.FILES.get('image')
            color_id = request.POST.get('color_name')
            color_name = get_object_or_404(ColorVariation, id=color_id)
            existing_product = Product.objects.filter(product_name=product_name, color_name=color_name).first()
            if existing_product:
                messages.info(request, f"{product_name} with {color_name} already exist")
            else:
                new_product =Product(product_name=product_name,description=description,price=price,product_qnty=product_qnty,image=image,category=category,color_name=color_name)
                new_product.save()
            check = [product_name,category_id,description,price,product_qnty,color_name]
            for values in check:
                if values == '':
                    messages.info(request,'some fields are empty')
                    return redirect('add_product')
                else:
                    pass
                    return redirect('display_product')
        except Exception as e:
            print("exception occured",str(e))
            pass
    return redirect('display_product')
    # return render(request,'dashboard_view/product_manager.html')
# def add_product(request):
#     if request.method == "POST":
#         forms = AddProductForm(request.POST)

#         if forms.is_valid():
#             forms.save()
#             # forms.save_m2m()
#             return redirect('display_product')
#     else:
#         forms = AddProductForm()
#     return render(request, 'dashboard_view/dashboard.html',{'form': forms})
# ADMIN EDIT A PRODUCT
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    colors = ColorVariation.objects.all()
    if request.method == "POST":
            product_name = request.POST.get('product_name')
            category_id = request.POST['category']
            category = get_object_or_404(Category, id=category_id)
            description = request.POST.get('description')
            price = request.POST.get('price')
            product_qnty = request.POST.get('product_qnty')
            image = request.FILES.get('image')
            color_id = request.POST['color_name']
            if color_id:
                try:
                    color_name = ColorVariation.objects.get(id=color_id)
                except ColorVariation.DoesNotExist:
                    raise Http404("ColorVariation does not exist")
            else:
                color_name = None
            # check = [product_name,category_id,description,price,product_qnty,color_name]
            # for values in check:
            #     if values == '':
            #         messages.info(request,'some fields are empty')
            #         return redirect('add_product')
            #     else:
            #         pass
            #         return redirect('display_product')
            # Update the product fields
            product.product_name = product_name
            product.category = category
            product.description = description
            product.price = price
            product.product_qnty = product_qnty
            product.color_name = color_name

            if image:
                product.image = image

            # Save the updated product
            product.save()
            messages.info(request,'success')
            return redirect('display_product')
        

    context = {
        'product': product,
        'categories': categories,
        'my_color': colors,
    }

    return render(request, 'dashboard_view/product_manager.html', context)

