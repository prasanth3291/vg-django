from django.db import models
from django.db.models.query import QuerySet
from category.models import category,Sub_category
from django.urls import reverse
from django.db.models import Avg,Count



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
# new here two more classes added for variation
class Color(models.Model):
    color_name=models.CharField( max_length=50)
    color_code=models.IntegerField()
    is_availabale=models.BooleanField(default=True)
    
    def __str__(self):
        return self.color_name
    
    
class Size(models.Model):
    size=models.CharField(max_length=50)
    is_availabale=models.BooleanField(default=True)
    
    def __str__(self):
        return self.size
    
class Discount(models.Model):
    name=models.CharField( max_length=50)   
    discount=models.PositiveIntegerField()
    def __str__(self):
        return self.name     
    
class Offer(models.Model):
    name=models.CharField( max_length=50)    
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    discount=models.ForeignKey(Discount,on_delete=models.CASCADE)    
    def __str__(self):
        return self.name  
class com_offers(models.Model):
    name=models.CharField( max_length=50)
    discount=models.PositiveIntegerField()
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    mimimum_value=models.IntegerField()
    maximum_discount=models.IntegerField()
    
    def __str__(self):
        return self.name  
        
    
    

class Product(softdelete):
    product_name    =models.CharField(max_length=100,unique=True)
    slug            =models.SlugField(max_length=200,unique=True)
    description     =models.TextField()    
    images          =models.ImageField(upload_to='pics/product')    
    is_available    =models.BooleanField(default=True)
    category        =models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    subcategory     = models.ForeignKey(Sub_category, on_delete=models.CASCADE,null=True)
    created_date    =models.DateTimeField(auto_now_add=True)
    modified_date   =models.DateTimeField(auto_now=True)
    discount        =models.ForeignKey(Discount,on_delete=models.CASCADE,null=True,blank=True) 
    offer           =models.ForeignKey(Offer,on_delete=models.CASCADE,null=True,blank=True) 

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    
    
    def __str__(self):
        return self.product_name    
    
    def averageReview(self):
        from acounts.models import ReviewRating        
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg    
    def count(self):
        from acounts.models import ReviewRating        
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
        return count

class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)    
    color           =models.ForeignKey(Color, on_delete=models.CASCADE,default="")
    size            =models.ForeignKey(Size, on_delete=models.CASCADE,default="")
    price           =models.IntegerField(default=0) 
    offer_price     =models.FloatField(blank=True,null=True)
    stock           =models.IntegerField(default=0) 
    is_active=models.BooleanField(default=True)
    created_date=models.DateField(auto_now_add=True)    
    def __str__(self):
       return self.product.product_name
       

       
    
    
 
