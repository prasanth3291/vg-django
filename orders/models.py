from django.db import models
from acounts.models import Acount,Coupons
from store.models import Product,Variation,Offer,com_offers
from carts.models import CartItem


class Payment(models.Model):
    user=models.ForeignKey(Acount, on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS=(
            ('New','New'),
            ('Accepted','Accepted'),
            ('Completed','Completed'),
            ('Cancelled','Cancelled')
            )  
    
    user=models.ForeignKey(Acount,on_delete=models.SET_NULL,null=True) 
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number=models.CharField(max_length=50) 
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50,blank=True)
    phone_number=models.CharField(max_length=50)
    email=models.EmailField( max_length=100)
    adress_line1=models.CharField(max_length=50)
    adress_line2=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    pin=models.CharField(max_length=50,blank=True)
    order_note=models.CharField(max_length=100,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField( max_length=10,choices=STATUS,default='New')
    ip=models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # offers and coupons
    offers=models.ForeignKey(com_offers, on_delete=models.CASCADE,blank=True,null=True)
    discount=models.DecimalField( max_digits=10, decimal_places=2,default=0)
    
    
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def __str__(self):
        return self.first_name
    def full_adress(self):
        return f"{self.adress_line1} {self.adress_line2}"
    

class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL ,blank=True,null=True)
    user=models.ForeignKey(Acount,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ForeignKey(Variation, on_delete=models.CASCADE,null=True) 
    quantity=models.IntegerField()
    product_price=models.FloatField()
    total=models.FloatField(null=True)
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name
    
class order_details(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)   
    original_total=models.FloatField()
    discount_from_coupons = models.FloatField(blank=True)
    discount_from_offers = models.FloatField(blank=True)
    sub_total = models.FloatField()
    tax = models.FloatField()
    grand_total = models.FloatField()
    status=models.BooleanField(default=False)
    
    
    
    
    
    

    
    
    

    
    
        
    