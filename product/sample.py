# Create your views here.
def productlist(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        
        products = Product.objects.all().order_by('id')
    
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }
    return render(request ,'dashboard/productlist.html',context)


def createproduct(request):
    
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        description = request.POST['product_description']
        brand_name = request.POST.get('brand')
        category_id = request.POST.get('category')
        
        try:
            image=request.FILES['image']
        except:
            image= ''
            
        

        # Validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product_list')
        if name == '' or price == '':
            messages.error(request, "Name or Price field is empty")
            return redirect('product_list')
        
        categorys = Category.objects.get(id=category_id)
        Brands = Brand.objects.get(brand_name=brand_name)
        

        # Save the product
        new_product = Product.objects.create(
            product_name=name,
            price=price,
            product_description=description,
            brand=Brands,
            category=categorys,
            
        )
        new_product.save()
        try:
            multiple_images = request.FILES.getlist('multiple_images')
            for image in multiple_images:
                image_model=Product_Image(product=new_product,image=image)
                image_model.save()
        except:
            multiple_images = ''
        
        if image:
            product_image = Product_Image.objects.create(
                product=new_product,
                image=image,
            )
            product_image.save()

        messages.success(request, 'Product added successfully')
        return redirect('productlist')

    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'categories': categories,
        'brands': brands,
        'new_product':new_product
    }
    return render(request, 'dashboard/productlist.html', context)

def deleteproduct(request,deleteproduct_id):
    pro = Product.objects.get(identification=deleteproduct_id)
    pro.delete()
    return redirect('productlist')

def editproduct(request, editproduct_id):
    if request.method == 'POST':
        pname = request.POST['product_name']
        pprice = request.POST['product_price']
        description = request.POST['product_description']
        brandname = request.POST.get('brand')
        category_id = request.POST.get('category')

        # Validation
        if pname == '' or pprice == '':
            messages.error(request, "Name or Price field is empty")
            return redirect('productlist')

        try:
            product = Product.objects.get(identification=editproduct_id)
            images = product.product_image_set.all()
            if images:
                for i, image in enumerate(images):
                    eimage = request.FILES.get(f'image{i+1}')
                    if eimage:
                        image.image = eimage
                        image.save()
        except Product.DoesNotExist:
            messages.error(request, "Product not found")
            return redirect('productlist')

        # Save
        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(brand_name=brandname)

        product.product_name = pname
        product.price = pprice
        product.product_description = description
        product.brand = brand
        product.category = category
        product.save()

        return redirect('productlist')
