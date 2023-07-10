from django.shortcuts import render, redirect
from .models import main_ad
from django.core.exceptions import ObjectDoesNotExist


def ad_management(request):
    if request.method == 'POST':
        main_image = request.FILES.get('main_image')
        main_head = request.POST.get('main_head')
        main_description = request.POST.get('main_description') 

        image1 = request.FILES.get('image1')
        price1 = request.POST.get('price1')
        description1 = request.POST.get('description1') 

        image2 = request.FILES.get('image2')
        price2 = request.POST.get('price2')
        description2 = request.POST.get('description2') 

        image3 = request.FILES.get('image3')
        price3 = request.POST.get('price3')
        description3 = request.POST.get('description3')

        # new_ad = main_ad.objects.get(id=1)
        new_ad, created = main_ad.objects.get_or_create()

        new_ad.main_image =main_image
        new_ad.main_head=main_head
        new_ad.main_description=main_description

        new_ad.image1=image1
        new_ad.price1 = price1
        new_ad.description1 =description1

        new_ad.image2=image2
        new_ad.price2 = price2
        new_ad.description2 =description2

        new_ad.image3=image3
        new_ad.price3 = price3
        new_ad.description3 =description3

        print(new_ad.main_image,'image')

        # new_ad =main_ad(main_image=main_image,main_head=main_head,main_description=main_description,image1=image1,price1=price1,description1=description1,image2=image2,price2=price2,description2=description2,image3=image3,price3=price3,description3=description3)
        new_ad.save()
        # main_ads = main_ad.objects.get(id = 1)
        context = {
            'main_ad' :new_ad,
        }
    else:
        try:
            new_ad = main_ad.objects.get(id = 1)
            # new_ad = main_ad.objects.get()
        except ObjectDoesNotExist:
            new_ad = None

        context = {
            'main_ad' :new_ad,
        }
        # return redirect('dashboard')
        return render(request, 'dashboard_view/ad_manager.html',context)
    return render(request, 'dashboard_view/ad_manager.html',context)