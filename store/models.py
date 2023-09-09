from django.db import models
from django.db.models.query import QuerySet
from category.models import category
from django.urls import reverse



class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class softdelete(models.Model):
    is_deleted=models.BooleanField(default=False)
    
    everything=models.Manager()
    objects=NonDeleted()
    
    def SoftDelete(self):
        self.is_deleted=True
        self.save()
    def restore(self):
        self.is_deleted=True
        self.save
    class Meta:
        abstract=True        


class Product(softdelete):
    product_name    =models.CharField(max_length=100,unique=True)
    slug            =models.SlugField(max_length=200,unique=True)
    description     =models.TextField()
    price           =models.IntegerField()
    images          =models.ImageField(upload_to='pics/product')
    stock           =models.IntegerField()
    is_available    =models.BooleanField(default=True)
    category        =models.ForeignKey(category,on_delete=models.CASCADE)
    created_date    =models.DateTimeField(auto_now_add=True)
    modified_date   =models.DateTimeField(auto_now=True)
    

    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    
    
    def __str__(self):
        return self.product_name
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)    
    
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)
    
variation_category_choice=(('color','color'),('size','size'),)    
    
class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)    
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateField(auto_now_add=True)
    
    objects=VariationManager()
    
    def __str__(self):
        return self.variation_value
    
    
    
    
    
# Create your models here.
