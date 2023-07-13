from django.shortcuts import render, redirect
from .models import main_ad
from django.core.exceptions import ObjectDoesNotExist


def ad_management(request):
    try:
        new_ad = main_ad.objects.first()
    except ObjectDoesNotExist:
        new_ad = None
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
       
        new_ad1, created = main_ad.objects.get_or_create()
    # main advertisement
        if main_image == None and new_ad != None:
            new_ad1.main_image =new_ad.main_image
        else:
            new_ad1.main_image =main_image
        if main_head == None and new_ad != None:
            new_ad1.main_head= new_ad.main_head
        else: 
            new_ad1.main_head= main_head
        if  main_description == None and new_ad != None:
            new_ad1.main_description=new_ad.main_description
        else:
            new_ad1.main_description=main_description
    # advertisement 1
        if image1 == None and new_ad != None:
            new_ad1.image1 = new_ad.image1
        else:
            new_ad1.image1 = image1
        if price1 == None and new_ad != None:    
            new_ad1.price1 = new_ad.price1
        else:
            new_ad1.price1 = price1
        if description1 == None and new_ad != None:
            new_ad1.description1 = new_ad.description1
        else:
            new_ad1.description1 = description1
    # advertisement 2
        if image2 == None and new_ad != None:
            new_ad1.image2 = new_ad.image2
        else:
            new_ad1.image2 = image2
        if price2 == None and new_ad != None:    
            new_ad1.price2 = new_ad.price2
        else:
            new_ad1.price2 = price2
        if description2 == None and new_ad != None:
            new_ad1.description2 = new_ad.description2
        else:
            new_ad1.description2 = description2
    # advertisement 3
        if image3 == None and new_ad != None:
            new_ad1.image3 = new_ad.image3
        else:
            new_ad1.image3 = image3
        if price3 == None and new_ad != None:    
            new_ad1.price3 = new_ad.price3
        else:
            new_ad1.price3 = price3
        if description3 == None and new_ad != None:
            new_ad1.description3 = new_ad.description3
        else:
            new_ad1.description3 = description3

        new_ad1.save()
        new_ad = new_ad1
        new_ad.save()
  
    context = {
        'main_ad' :new_ad,
    }

    return render(request, 'dashboard_view/ad_manager.html',context)