from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from store.models import Product,Variation,Color,Size
from carts.models import Carts,CartItem,UserCoupons
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from acounts.models import Adress,Coupons
from django.contrib import messages,auth
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
    tax=0   
    grand_total=0       
    status=False
    used=False
    current_user=request.user
    saved_addresses = Adress.objects.filter(user=current_user)
    #if the request method is post.ie when someone aplly coupon
    if request.method=='POST':
        
        user=request.user
        coupon_id=request.POST.get('selected_coupon')#fetch the coupen id from form
        valid_coupon=get_object_or_404(Coupons,id=coupon_id)# get the corresponding coupon
        coupons=Coupons.objects.filter(user=request.user)#fetch all coupons of the user    
        user_coupons=UserCoupons.objects.filter(user=request.user)#get user all applied coupon if any
        if not UserCoupons.objects.filter(user=request.user,coupon=valid_coupon).exists():                         
                discount=valid_coupon.discount
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
                messages.error(request,"Coupon Already availed")                
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
                'used':used        
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
            total=total-(total*discount)/100                    
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
        'user_coupon':user_coupon        
                }       
    else:
    # reqst post method failed then part
       
        coupons=Coupons.objects.filter(user=request.user)     
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
            'coupons':coupons        
                    }                  
    return render(request,'store/checkout.html',context)
        

# Create your views here.
