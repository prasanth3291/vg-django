from django.db import models
from store.models import Product
from store.models import Variation
from acounts.models import Acount



class Carts(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField( auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    user=models.ForeignKey(Acount, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)   
    cart=models.ForeignKey(Carts,on_delete=models.CASCADE,null=True) 
    variations=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
   
    
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product    

# Create your models here.
