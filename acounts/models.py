from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from twilio.rest import Client


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
        


class Acount(AbstractBaseUser):
    first_name    = models.CharField( max_length=50)
    last_name     = models.CharField( max_length=50)
    username     = models.CharField(max_length=50,unique=True)
    email         = models.EmailField( max_length=254,unique=True)
    phone_number  = models.CharField(max_length=50)
    
# required fields as its custome user model
    date_joined   = models.DateTimeField(auto_now_add=True)
    last_login    = models.DateTimeField(auto_now_add=True)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
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
    user=models.ManyToManyField(Acount,blank=True,null=True)
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    
    
    
# Create your models here.
