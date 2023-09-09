from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from store.models import Product,Variation
from carts.models import Carts,CartItem
from django.core.exceptions import ObjectDoesNotExist

def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    




def add_cart(request,product_id):
    
    product=Product.objects.get(id=product_id)
    product_variation=[]
    if request.method =='POST':
       for item in request.POST:
           key=item 
           value=request.POST[key]
        
           try:
               variation=Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
               product_variation.append(variation)
           except:
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
            existing_variation=item.variations.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)
        print(existing_variation_list)
        
        if product_variation in existing_variation_list:
            # increase the product quantity
            index=existing_variation_list.index(product_variation)
            item_id=id[index]
            item=CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            item.save()
            
        else:
            # create a cart item
            item=CartItem.objects.create(product=product,quantity=1,cart=cart)
            item.variations.clear()
            if len(product_variation) > 0:
               
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item=CartItem.objects.create(
            product=product,
            quantity =1,
            cart =cart
            
        )  
        cart_item.variations.clear()
        if len(product_variation)>0:
          
            cart_item.variations.add(*product_variation)
            cart_item.save()
    return  redirect('carts')

        
         
def carts(request,total=0,quantity=0,cart_items=None):   
    tax=0
    grand_total=0
    
    try:
        cart=Carts.objects.get(cart_id=cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True).order_by('product')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax=(total * 18 )/100
        grand_total=total+tax    
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
    cart=Carts.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    
    
    try:
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
    cart=Carts.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
    cart_item.delete()
    return redirect('carts')      
        

# Create your views here.
