from django.shortcuts import render,redirect
from .forms import RegistrationForms
from.models import Acount
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login
from django.shortcuts import HttpResponse

# user verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

#new 
import os
from twilio.rest import Client
import random

# for cart checkout
from carts.views import Carts,cart_id
from carts.models import Carts,CartItem
import requests

def generate_random_otp():
    # Generate a 6-digit random OTP
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return otp




def register(request):
    if request.method=='POST':
        form=RegistrationForms(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']            
            last_name=form.cleaned_data['last_name']        
            phone_number=form.cleaned_data['phone_number']            
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]        
            user=Acount.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            # acount activation
            token=default_token_generator.make_token(user)
            current_site=get_current_site(request)
            mail_subject='please activate your acount'
            message=render_to_string('acounts/acount_verification_email.html',{
                                        'user':user,
                                      'domain':current_site,
                                      'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                      'token':token,  
                                    })                               
                                      
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            
            #new
            otp=generate_random_otp()
            account_sid = "ACd61c3ec36ca81a50af865490b6342a4a"
            auth_token = "7e218b3d29fa75c7bbee951db0815b88"
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                     body=render_to_string('acounts/acount_verification_email.html',{
                                        'user':user,
                                      'domain':current_site,
                                      'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                      'token':token,  
                                    })                               
                                      ,
                     from_='+15862570025',
                     to=phone_number
                 )
            print(message.sid)    
            send_email.send()
            
            # messages.success(request,'Thank you for regestering with us,we have sent an verification link to your Email adress.Please verify it..')
            return redirect ('/acounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForms()        
    
    context={
        'form': form
    }
    
    
    return render(request,'acounts/register.html',context)

from django.views.decorators.cache import never_cache
@never_cache
def login(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_superadmin:
                return render(request,'admins/dashboard.html')
        else:
            
            return redirect ('user_dashboard')
    
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=auth.authenticate(email=email,password=password)
        
        if user is not None:            
            try:
                cart=Carts.objects.get(cart_id=cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    #getting the product variation byt product id 
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation)) 
                    
            # exis. variation --> from database            
            # current variations--> from product variation            
            #item id--> from db
                    cart_item=CartItem.objects.filter(user=user)
                    existing_variation_list=[]    
                    id=[]    
                    for item in cart_item:
                        existing_variation=item.variations.all()
                        existing_variation_list.append(list(existing_variation))
                        id.append(item.id)
                        
                    for pr in product_variation:    
                        if pr in existing_variation_list:
                            indx=existing_variation_list.index(pr)
                            item_id=id[indx]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user=user
                            item.save()
                        else:    
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
                
            except:
                pass    
            
            auth.login(request,user)
            
            if user.is_superadmin:
                return render(request,'admins/dashboard.html')
            else:
                messages.success(request,'Successfully signed in')
                url=request.META.get('HTTP_REFERER')
                try:
                    query=requests.utils.urlparse(url).query
                    
                    print('qry-->',query)
                    # we will split qry
                    params=dict(x.split('=') for x in query.split('&') )
                    if 'next' in params:
                        nextPage=params['next']
                        print('ne',nextPage)
                        return redirect(nextPage)
                    else:
                        return redirect ('user_dashboard')
                except:
                    pass    
                    
        else:
            messages.error(request,'invalid login credentials')
            return redirect ('login')
    return render(request,'acounts/login.html')


@login_required(login_url='login')
@never_cache
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('login')


# activate
def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Acount._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Acount.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations Your Acount is activated')          
        return redirect('login')
    
    else:
        messages.error(request,'Invalid link')
        return redirect ('register')
    
    
def user_dashboard(request):
    return render(request,'acounts/user_dashboard.html')


def forgot_password(request):   
    if request.method == 'POST':
        email=request.POST['email']
        if Acount.objects.filter(email=email).exists():
            user=Acount.objects.get(email__iexact=email)
            
            #reset password email
            token=default_token_generator.make_token(user)
            current_site=get_current_site(request)
            mail_subject='Reset your Password'
            message=render_to_string('acounts/reset_password_email.html',{
                                        'user':user,
                                      'domain':current_site,
                                      'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                      'token':token,  
                                    })                               
                                      
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()            
            messages.success(request,'Password reset email has sent to your email adress.')
           
            return redirect('login')
            
            
        else:
            messages.error(request,'Account does not exists')   
            return redirect('forgot_password')
    return render(request,'acounts/forgot_password.html')
def resest_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Acount._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Acount.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):    
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('reset_password') 
    else:
        messages.error(request,'This link has been expired')   
        return redirect('login')     
    
def reset_password(request):
    if request.method=='POST':
        password=request.POST['create_password']
        confirm_password=request.POST['confirm_password']
        
        if password==confirm_password:
            uid=  request.session['uid']
            user=Acount.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
            
        else:
            messages.error(request,'Password do not match')   
            return redirect('reset_password')
            
    return render(request,'acounts/reset_password.html')
    
        
        
        
        
        
        
        
        
        
# Create your views here.


