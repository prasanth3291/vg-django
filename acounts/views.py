from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForms,UserForm,UserProfileForm,AdressForm
from.models import Acount,UserProfile,Adress,Coupons,Wishlist
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login
from django.shortcuts import HttpResponse
from orders.models import Order,Payment,OrderProduct
from store.models import Product,Variation
import urllib.parse

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
            auth_token = "ec37d52f13ccb00c5f40188b9a01ba36"
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
                        variation=item.variations
                        product_variation.append(variation) 
                    
            # exis. variation --> from database            
            # current variations--> from product variation            
            #item id--> from db
                    cart_item=CartItem.objects.filter(user=user)
                    existing_variation_list=[]    
                    id=[]    
                    for item in cart_item:
                        existing_variation=item.variations
                        existing_variation_list.append(existing_variation)
                        id.append(item.id)
                        
                    for var in product_variation:    
                        if var in existing_variation_list:
                            indx=existing_variation_list.index(var)
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
                messages.success(request,'User Successfully signed in')
                url=request.META.get('HTTP_REFERER')
                print('url=',url)
                next_url = request.GET.get('next')
                print('next',next_url)
                try:
                    query=requests.utils.urlparse(url).query
                  #  next_url = request.GET.get('next', 'wish_list')
                   # print(next_url)
                    
                    if query:
                        print('qry-->',query)
                        # we will split qry
                        params=dict(x.split('=') for x in query.split('&') )    
                        
                        # this is for wishlist                        
                        url_value=params['next']      
                        if 'add_wish_list' in url_value:            
                            parsed_url = urllib.parse.urlparse(url)                           
                            print(parsed_url)
                            next_param = urllib.parse.unquote(parsed_url.query.split('=')[1])                          
                            return  redirect(next_param)
                                         
                        elif 'next' in params:                            
                            nextPage=params['next']
                            print('ne',nextPage)
                            return redirect(nextPage)
                        else:                        
                            return redirect ('user_dashboard')
                    else:
                        return redirect('user_dashboard')    
                except:
                    print('hai')
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
        UserProfile.objects.create(user=user) 
        return redirect('login')
    
    else:
        messages.error(request,'Invalid link')
        return redirect ('register')
    

@login_required(login_url='login')    
def user_dashboard(request):
        orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
        orders_count=orders.count()
        context={
                'orders_count':orders_count
            }
            
        print('order',orders_count)
        return render(request,'acounts/user_dashboard.html',context)


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

@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    order_products=OrderProduct.objects.all()
    context={
        'orders':orders,
        'order_product':order_products
    }

    return render(request,'acounts/my_orders.html',context)

def or_pr_detail(request, order_product_id):
    # Fetch the specific order product based on the provided ID
    order_product = get_object_or_404(OrderProduct, id=order_product_id)

    # You can also fetch related order details if needed
    order = order_product.order

    context = {
        'order_product': order_product,
        'order': order,  # Include order details if needed
    }

    return render(request, 'acounts/order-product-detail.html', context)    

@login_required(login_url='login')        
def edit_profile(request):      
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':       
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')        
    else:
            user_form=UserForm(instance=request.user)
            profile_form=UserProfileForm(instance=userprofile)
            
    context={
            'user_form':user_form,
            'profile_form':profile_form,
            'userprofile':userprofile
        }   
    return render(request,'acounts/edit_profile.html',context)    
 
@login_required(login_url='login')
def change_password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
        user=Acount.objects.get(username__exact=request.user.username)
        
        if new_password==confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request,'Password has been changed successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Enter valid current password')
                return redirect('change_password')
        else:
                messages.error(request,'Password doent match')
                return redirect('change_password')    
    return render(request,'acounts/change_password.html')   

def manage_adress(request):
    user=request.user
    adresses=Adress.objects.filter(user=user)
    context={
        'adresses':adresses
    }
    return render(request,'acounts/manage_adress.html',context)

def add_adress(request):
    if request.method=='POST':
        user        =request.user
        name        =request.POST.get('name')
        phone_number=request.POST.get('phone_number')
        adress_line1=request.POST.get('adress_line1')
        adress_line2=request.POST.get('adress_line2')
        city        =request.POST.get('city')
        state       =request.POST.get('state')
        country     =request.POST.get('country')
        pincode     =request.POST.get('pin')
        
        
        adress= Adress(
                user        =user,
                name        =name,
                phone_number=phone_number,
                adress_line1=adress_line1,
                adress_line2=adress_line2,
                city        =city,
                state       =state,
                country     =country,
                pin    =pincode
                 )
        adress.save()
    return redirect('manage_adress')

def edit_adress(request,adress_id):
    print('first')
    adress=Adress.objects.get(id=adress_id)
    print('second')
    #copt
    if request.method=='POST':      
        print('got ir') 
        adress_form=AdressForm(request.POST,instance=adress)
        if adress_form.is_valid():
            adress_form.save()
        
            messages.success(request,'Your profile has been updated')
            return redirect('manage_adress')        
    else:
            adress_form=AdressForm(instance=adress)
   
    context={
        'adress':adress,
        'adress_form':adress_form
    }
    
    return render(request,'acounts/edit_adress.html',context)

def delete_adress(request,adress_id):
    adress=Adress.objects.get(id=adress_id)
    adress.delete()
    return redirect('manage_adress')

def coupons(request):
    user_coupons = Coupons.objects.filter(user=request.user)
    context={
        'user_coupons':user_coupons
    }
    return render(request,'acounts/coupons.html',context)

# the method to implement wishlist
@login_required(login_url='login')
def add_wish_list(request, product_id=None):
    next_url = request.GET.get('next', 'wish_list')
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    print('nu=',next_url)
    
    url=request.META.get('HTTP_REFERER')
    print('url=',url)
    
    # Check if the product is already in the user's wishlist
    if Wishlist.objects.filter(user=user, products=product).exists():
        Wishlist.objects.filter(user=user, products=product).delete()
    else:
        variations = Variation.objects.filter(product=product)
        variation = variations.first()
        Wishlist.objects.create(
            user=user,
            products=product,
            variation=variation,
        )

    return redirect(next_url)

    
            
@login_required(login_url='login')        
def wish_list(request):    
    if request.user.is_authenticated:    
        user=request.user
        wish_lists=Wishlist.objects.filter(user=user)
        context={
        'wish_lists':wish_lists
            }
        return render(request,'acounts/wishlist.html',context)
    
            

    
    

    
            
        
        
        
        
        
        
        
# Create your views here.


