from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from store.models import Product,Variation,Color,Size
from carts.models import Carts,CartItem,UserCoupons
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from acounts.models import Adress,Coupons
from django.contrib import messages,auth
from datetime import datetime
def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    

def add_cart(request,product_id):
    
    current_user=request.user
    product=Product.objects.get(id=product_id) # here use variations instead prodcut
    # now fetch all variations of that product
    variation=None

    # if the user is authenticated:
    if current_user.is_authenticated:
        #product_variation=[]
        if request.method =='POST':
            print("authe user inside try block")
            color_id=request.POST['color']    
            print("1",color_id)    
            size_id=request.POST['size']    
            print("2",size_id)
            
            try:
                print('here also')
                color = get_object_or_404(Color, color_name=color_id)
                size = get_object_or_404(Size, size=size_id)
                variation=Variation.objects.get(product=product, color=color, size=size)# got the exact variation
                #product_variation.append(variation)
                print(variation)
                print(variation.price)
               
            except:
                print("first try block not worked its except block")
                pass  
        #print(product_variation)
        is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:            
            print('cart item exusts')
            cart_item=CartItem.objects.filter(product=product,user=current_user)
            # exis. variation --> from database            
            # current variations--> from product variation
            
            #item id--> from db
            existing_variation_list=[]    
            id=[]    
            for item in cart_item:
                existing_variation=item.variations
                existing_variation_list.append(existing_variation)
                id.append(item.id)
          
            
            if variation in existing_variation_list:
                # increase the product quantity
                index=existing_variation_list.index(variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
                
            else:
                # create a cart item
                item=CartItem.objects.create(product=product,quantity=1,user=current_user,variations=variation)               
                item.save()
                print(variation.price)
        else:
            print('cart item not exists')
            cart_item=CartItem.objects.create(
                product=product,                
                quantity =1,
                user=current_user,
                variations=variation  
            )  
            cart_item.save()
        print("yes")
        print(variation.price)        
        return  redirect('carts')
    

    # if the user is not authenticated    
    else:    
        if request.method =='POST':
            print("got inside")
            color_id=request.POST['color']        
            size_id=request.POST['size']   
            
            try:
                print('here also')
                color = get_object_or_404(Color, color_name=color_id)
                size = get_object_or_404(Size, size=size_id)
                variation=Variation.objects.get(product=product, color=color, size=size)# got the exact variation
                #product_variation.append(variation)
                print(variation)
                print(variation.price)
               
            except:
                print("i came here")
                pass  
            
        try:
            cart=Carts.objects.get(cart_id=cart_id(request))
        except Carts.DoesNotExist:
            cart=Carts.objects.create(cart_id=cart_id(request))
        cart.save()   
        
        is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:            
            cart_item=CartItem.objects.filter(product=product,cart=cart)
            # exis. variation --> from database            
            # current variations--> from product variation
            
            #item id--> from db
            existing_variation_list=[]    
            id=[]    
            for item in cart_item:
                existing_variation=item.variations
                existing_variation_list.append(existing_variation)
                id.append(item.id)
          
            
            if variation in existing_variation_list:
                # increase the product quantity
                index=existing_variation_list.index(variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
                
            else:
                # create a cart item
                item=CartItem.objects.create(product=product,quantity=1,cart=cart,variations=variation)               
                item.save()
        else:
            print('entered')
            cart_item=CartItem.objects.create(
                product=product,                
                quantity =1,
                cart=cart,
                variations=variation  
            )  
            cart_item.save()
        print("yes")
        print(variation)        
        return  redirect('carts')


        
         
def carts(request,total=0,quantity=0,cart_items=None):   
    tax=0
    grand_total=0
    
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('product')
            
        else:   
        
            cart=Carts.objects.get(cart_id=cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True).order_by('product')
            
        for cart_item in cart_items:  
            price=0          
            try:
                if cart_item.variations.offer_price:
                    price=cart_item.variations.offer_price
                else:
                    price=cart_item.variations.price   
            except:
                pass         
                
            total += (price * cart_item.quantity)
            quantity += cart_item.quantity
        tax=(total * 18 )/100
        grand_total=total+tax    
        grand_total=round(grand_total,2)
    except ObjectDoesNotExist:
            pass    
    context= {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
        
    }
    
    return render(request,'store/cart.html',context)

def remove_cart(request,product_id,cart_item_id):
    
    product=get_object_or_404(Product,id=product_id)
    
    
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:   
            cart=Carts.objects.get(cart_id=cart_id(request)) 
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity >1 :
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass        
            
    return redirect('carts')  

def remove_cart_item(request,product_id,cart_item_id):
    
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:    
        cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
        cart=Carts.objects.get(cart_id=cart_id(request))
    cart_item.delete()
    return redirect('carts')     


@login_required(login_url='login') 
def checkout(request,total=0,quantity=0,cart_items=None): 
    total=0
    discount=0
    discount_value=0
    tax=0   
    original_total=0
    offer_discount=0
    grand_total=0       
    status=False
    used=False
    current_user=request.user
    saved_addresses = Adress.objects.filter(user=current_user)
    coupons=Coupons.objects.all()
    #if the request method is post.ie when someone aplly coupon
    if request.method=='POST':        
        user=request.user        
        # form here,check that the coupon entered is 1) active 2)date expired #3)count>0     
             
        valid_coupon=None
        try:
            coupon_name=request.POST.get('coupon_code')#fetch the coupen id from form  
            valid_coupon=get_object_or_404(Coupons,name=coupon_name)# get the corresponding coupon
        except:
            messages.error(request,"Invalid coupon name",extra_tags='coupon')
            return redirect('checkout')
            
        if valid_coupon:           
            print('coupon')            
            #check the coupon is expired                       
            today=datetime.now().date()
            print(today)
            valid_date=valid_coupon.valid_to
            print(valid_date)
            #check for the valid date            
            if today>valid_date:
                messages.error(request,"Coupon is expired",extra_tags='coupon')
                return redirect('checkout')            
            #if coupon used and count became zero                
            elif valid_coupon.coupon_count<1:                
                messages.error(request,"Coupon is expired",extra_tags='coupon')
                return redirect('checkout')
            #if everything satisfies
            else:  
                coupon_discount          =valid_coupon.discount
                coupon_mv                =valid_coupon.minimum_amount
                coupon_max_discount_value=valid_coupon.maximum_discount            
        #coupons=Coupons.objects.filter(user=request.user)#fetch all coupons of the user            
        user_coupons=UserCoupons.objects.filter(user=request.user)#get user all applied coupon if any
        if not UserCoupons.objects.filter(user=request.user,coupon=valid_coupon).exists():                       
                user_coupon=UserCoupons.objects.create(
                    coupon=valid_coupon,
                    user=request.user,
                    applied=True,
                    is_active=True
               )
                user_coupon.save
                status=True            
        else:
            user_coupon=get_object_or_404(UserCoupons,coupon=valid_coupon,user=request.user)
            if user_coupon.is_active:             
                discount=valid_coupon.discount
                status=True
                user_coupon.applied=True
                user_coupon.save()
            else:
                used=True
                messages.error(request,"Coupon Already availed",extra_tags='coupon')                
                #here nee to alert the coupon is already used 
                try:
                    if request.user.is_authenticated:          
                        cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('product')            
                    else:  
                        cart=Carts.objects.get(cart_id=cart_id(request))
                        cart_items=CartItem.objects.filter(cart=cart,is_active=True).order_by('product')
                    for cart_item in cart_items:                        
                        price=cart_item.variations.offer_price if cart_item.variations.offer_price is not None else cart_item.variations.price
                        total += (price * cart_item.quantity)
                        quantity += cart_item.quantity       
                        try:
                            original_total+=cart_item.variations.price*cart_item.quantity
                            offer_discount+=(cart_item.variations.price-cart_item.variations.offer_price)*cart_item.quantity
                        except:
                            pass                      
                    tax=(total * 18 )/100
                    grand_total=total+tax
                    total = round(total, 2)
                    tax = round(tax, 2)    
                    grand_total = round(grand_total, 2)
                except ObjectDoesNotExist:
                    pass    
                context= {
                'total':total,
                'quantity':quantity,
                'cart_items':cart_items,
                'tax':tax,
                'grand_total':grand_total,
                'saved_addresses':saved_addresses,
                'coupons':coupons,
                'user_coupon':user_coupon ,
                'used':used,
                'original_total':original_total,
                'offer_discount':offer_discount        
                    }                  
                return render(request,'store/checkout.html',context)                             
        try:
            if request.user.is_authenticated:          
                cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('product')            
            else:  
                cart=Carts.objects.get(cart_id=cart_id(request))
                cart_items=CartItem.objects.filter(cart=cart,is_active=True).order_by('product')
            for cart_item in cart_items:
                price=cart_item.variations.offer_price if cart_item.variations.offer_price is not None else cart_item.variations.price
                total += (price * cart_item.quantity)
                quantity += cart_item.quantity
                try:
                    original_total+=cart_item.variations.price*cart_item.quantity
                    offer_discount+=(cart_item.variations.price-cart_item.variations.offer_price)*cart_item.quantity
                except:
                    pass    
                #here store its original price and offer discount
            # from here check for coupons  
            if valid_coupon:  
                # check the total price meet the minium purchase value
                if total>=coupon_mv:
                    discount_value=total*coupon_discount/100
                    # check the discount value exceeds maxium discount
                    if coupon_max_discount_value<=discount_value:
                        discount_value=coupon_max_discount_value
                        messages.success(request,f"Maximum discount is {coupon_discount}",extra_tags='coupon')                        
                    total=total-discount_value                    
                    tax=(total * 18 )/100
                    total = round(total, 2)
                    tax = round(tax, 2)
                    grand_total=total+tax   
                    grand_total=round(grand_total, 2) 
                #coupon apply minium value doesnt meet    
                else:
                    user_coupon.applied=False
                    user_coupon.save()
                    messages.error(request,f"Minium purchase value for this coupon is {coupon_mv}",extra_tags='coupon')  
                    total = round(total, 2)
                    tax=(total * 18 )/100
                    tax = round(tax, 2)
                    grand_total=total+tax   
                    grand_total=round(grand_total, 2)   
            else:                
                tax=(total * 18 )/100
                total = round(total, 2)
                tax = round(tax, 2)
                grand_total=total+tax   
                grand_total=round(grand_total, 2) 
            
        except ObjectDoesNotExist:
                pass    
        context= {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'saved_addresses':saved_addresses,
        'coupons':coupons,
        'valid_coupon':valid_coupon,
        'status':status,
        'user_coupon':user_coupon,
        'coupon_mv':coupon_mv,
        'coupon_max_discount_value':coupon_max_discount_value,
        'coupon_discount':coupon_discount,
        'discount_value':discount_value,
        'original_total':original_total,
        'offer_discount':offer_discount
                
                }       
    else:
    # reqst post method failed then part
       
        user_coupons=UserCoupons.objects.filter(user=request.user,applied=True,is_active=True)    
        if user_coupons:    
            for user_coupon in user_coupons:
                user_coupon.applied=False   
                user_coupon.save()
        try:
            if request.user.is_authenticated:          
                cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('product')            
            else:  
                cart=Carts.objects.get(cart_id=cart_id(request))
                cart_items=CartItem.objects.filter(cart=cart,is_active=True).order_by('product')
            for cart_item in cart_items:
                    price=cart_item.variations.offer_price if cart_item.variations.offer_price is not None else cart_item.variations.price
                    total += (price * cart_item.quantity)
                    quantity += cart_item.quantity     
                    try:
                        original_total+=cart_item.variations.price*cart_item.quantity
                        offer_discount+=(cart_item.variations.price-cart_item.variations.offer_price)*cart_item.quantity
                    except:
                        pass                         
            tax=(total * 18 )/100
            grand_total=total+tax
            total = round(total, 2)
            tax = round(tax, 2)    
            grand_total=round(grand_total,2)
        except ObjectDoesNotExist:
            pass    
        context= {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total,
            'saved_addresses':saved_addresses,
            'coupons':coupons,
            'original_total':original_total,
            'offer_discount':offer_discount        
                    }                  
    return render(request,'store/checkout.html',context)
        

# Create your views here.
