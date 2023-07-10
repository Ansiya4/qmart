from django.db import models

# Create your models here.
class main_ad(models.Model):

    main_image = models.ImageField(max_length=50, blank=True, null=True)
    main_head = models.TextField(unique=True) 
    main_description = models.TextField(max_length=100, unique=True) 

    image1 = models.ImageField(max_length=50, blank=True, null=True)
    price1 = models.IntegerField(unique=True,null=True) 
    description1 = models.TextField(max_length=100, unique=True) 

    image2 = models.ImageField(max_length=50,blank=True, null=True)
    price2 = models.IntegerField(unique=True,null=True) 
    description2 = models.TextField(max_length=100, unique=True, default='') 

    image3 = models.ImageField(max_length=50,blank=True, null=True)
    price3 = models.IntegerField(unique=True,null=True) 
    description3 = models.TextField(max_length=100, unique=True) 


