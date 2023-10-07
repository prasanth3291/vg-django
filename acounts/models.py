from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from twilio.rest import Client
from store.models import Product,Variation
import random,string
from decimal import Decimal

class MyacountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an Email adress')
        if not username:
            raise ValueError('User must have a unsername')
        user= self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            
            
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user =self.create_user( 
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name 
        ) 
          
        user.is_admin = True
        user.is_active= True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
        
# create a random code
def generate_unique_referral_code():
    # Generate a random code of 5 or 6 characters
    code_length = 6
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(code_length))

    # Check if the generated code is unique
    while Referal_code.objects.filter(code=code).exists():
        code = ''.join(random.choice(characters) for _ in range(code_length))

    return code

class Acount(AbstractBaseUser):
    first_name = models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField( max_length=254,unique=True)
    phone_number = models.CharField(max_length=50)    
    Referal_code=models.CharField( max_length=6,unique=True,default=generate_unique_referral_code) 

# required fields as its custome user model
    date_joined  = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']
    
    objects=MyacountManager()
    
    def __str__(self):
        return self.email
    def has_perm(self,perm,object=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True
    
class UserProfile(models.Model):
    user=models.OneToOneField(Acount, on_delete=models.CASCADE)    
    adress_line1=models.CharField(blank=True, max_length=50)
    adress_line2=models.CharField(blank=True, max_length=50)
    profile_picture=models.ImageField(blank=True, upload_to='userprofile/',default="/static/images/logo vg.jpg") 
    city=models.CharField(blank=True, max_length=50)
    state=models.CharField(blank=True, max_length=50)
    country=models.CharField(blank=True, max_length=50)
    
    def __str__(self):
        return self.user.first_name
    
    def full_adress(self):
        return f'{self.adress_line1} {self.adress_line2}'
    
    
class Adress(models.Model):
    user=models.ForeignKey(Acount,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)    
    adress_line1=models.CharField(blank=True,max_length=50)
    adress_line2=models.CharField(blank=True,max_length=50)
    city=models.CharField( max_length=50)
    state=models.CharField( max_length=50)
    country=models.CharField( max_length=50)
    pin=models.CharField( max_length=50)
    phone_number=models.CharField(max_length=50,default='')
    email= models.EmailField( max_length=254,default="")
    
    
class Coupons(models.Model):
    name=models.CharField(max_length=50)
    discount=models.PositiveIntegerField()
    valid_from=models.DateField()
    valid_to=models.DateField()
    minimum_amount=models.IntegerField(default=5000)
    maximum_discount=models.IntegerField(default=5000)
    coupon_count=models.IntegerField() 
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
# wishlist model
class Wishlist(models.Model):
    user=models.ForeignKey(Acount, on_delete=models.CASCADE)    
    products=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation=models.ForeignKey(Variation, on_delete=models.CASCADE)   
    added_at=models.DateField(auto_now_add=True)
    def __str__(self):
         return f"{self.user.username}'s Wishlist Item: {self.products.product_name}  "
     

     
# refereal code mo     
class Referal_code(models.Model):
    code=models.CharField( max_length=6)   
    referrer_user = models.ForeignKey(Acount, on_delete=models.CASCADE, related_name='referral_code_given')
    referred_user = models.ForeignKey(Acount, on_delete=models.CASCADE, blank=True, null=True, related_name='referral_code_received')  
    gift_money=models.IntegerField()
    is_activated=models.BooleanField(default=False) 
       
    
    def __str__(self):
        return self.code
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)     
    user = models.ForeignKey(Acount,on_delete=models.CASCADE)   
    subject = models.CharField( max_length=100,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField( max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)  
    def __str__(self):
        return self.subject    
    
    
    
class Wallet(models.Model):
    user = models.OneToOneField(Acount, on_delete=models.CASCADE)    
    balance = models.DecimalField( max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return f"{self.user.username}'s wallet"
    
    def add_fund(self,amount):
        if amount > 0:
            self.balance += Decimal(amount)
            self.save()
            
    def deduct_fund(self,amount):
        if amount>0:
            self.balance -= Decimal(amount)
            self.save()        
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)     
    amount = models.DecimalField( max_digits=10, decimal_places=2)
    balance=models.DecimalField( max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250,blank=True)  
    
    def __str__(self):
        return f"Transaction for {self.wallet.user.username} - {self.amount}"
    


     
   


    
    
    
# Create your models here.
