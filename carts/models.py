from django.db import models
from store.models import Product
from store.models import Variation
from acounts.models import Acount,Coupons



class Carts(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField( auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    user=models.ForeignKey(Acount, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)   
    cart=models.ForeignKey(Carts,on_delete=models.CASCADE,null=True) 
    variations=models.ForeignKey(Variation, on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
   
    
    
    def sub_total(self):
        if self.variations.offer_price:
            return self.variations.offer_price * self.quantity
        else:            
            return self.variations.price * self.quantity
        
    def sub_total_actual(self):  
        return self.variations.price * self.quantity  
    
    def __unicode__(self):
        return self.product    

# Create your models here.
class UserCoupons(models.Model):
    coupon=models.ForeignKey(Coupons,on_delete=models.CASCADE)    
    applied=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)  
    user=models.ForeignKey(Acount, on_delete=models.CASCADE,blank=True)
    
    def __str__(self):
        return self.coupon.name