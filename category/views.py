from django.shortcuts import render,redirect
from .models import Category
from django.contrib import messages
from django.shortcuts import get_object_or_404
# from products.models import Product
from django.core.exceptions import ValidationError

def category_manager(request):
    categ = Category.objects.all()
    context = {
        'category' : categ, 
    }
    return render(request,'dashboard_view/category_manager.html',context)

# ADMIN ADD CATEGORY
def add_category(request):
    if request.method == "POST":
        category_name= request.POST.get('category_name')
        description=request.POST.get('description')
        category_image=request.FILES.get('category_image')
    
        new_category =Category(category_name=category_name, description=description,category_image=category_image)
        new_category.save()
        print(new_category,"bbbbbbbbbbb")
        messages.success(request, 'Category added successfully.')
        return redirect('dashboard')

    return render(request,'dashboard_view/addCategory.html')



def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        category_image = request.FILES.get('category_image')

        try:
            # Validate the data
            if not category_name:
                messages.info(request,"Name field can't be empty")
            if not description:
                messages.info(request,"Add Description")

            # Update the category
            category.category_name = category_name
            category.slug = slug
            category.description = description
            if category_image:
                category.category_image = category_image
            # category.full_clean()  # Perform model-level validation
            category.save()
            messages.info(request,"Added Successfully")
            return redirect('dashboard')

        except:
            messages.info(request,"Error occured")
            # Handle validation errors
            pass

    context = {'category': category}
    return render(request, 'dashboard_view/addCategory.html', context)




# def edit_category(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     if request.method == "POST":
#         category_name = request.POST.get('category_name')
#         slug = request.POST.get('slug')
#         description = request.POST.get('description')
#         category_image = request.FILES.get('category_image')

#         category.category_name = category_name
#         category.slug = slug
#         category.description = description
#         if category_image:
#             category.category_image = category_image
#         category.save()
#         return redirect('dashboard')
#     context = {'category': category}
#     return render(request, 'dashboard_view/addCategory.html', context)

    