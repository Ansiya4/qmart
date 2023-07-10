from django.db import models
from category.models import Category
from django.utils.text import slugify

# Create your models here.
class ColorVariation(models.Model):
    color_name = models.CharField(max_length=50)

    def __str__(self):
        return self.color_name
class Product(models.Model):
    # product_id = models.AutoField(unique=True)
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description= models.TextField(max_length=50)
    # price = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product_qnty=models.IntegerField(default=None)
    image = models.ImageField(max_length=50, unique=True)
    is_available = models.BooleanField( default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now= True)
    color_name = models.ForeignKey(ColorVariation, on_delete=models.CASCADE,null= True)
    # slug = models.CharField(max_length=50, unique=True)
    # def save(self, *args, **kwargs):
    #     # generate slug field from name field if slug is empty
    #     if not self.slug:
    #         self.slug = slugify(self.product_name)
    #     super(Product, self).save(*args, **kwargs)
                                  
    def __str__(self):
        return self.product_name

