from django.urls import reverse
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    category_name= models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='photos/categories/')
    
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def get_url(self):
        return reverse('product_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
