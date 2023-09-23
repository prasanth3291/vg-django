from django.shortcuts import render,get_object_or_404,redirect
from.models import Product,Variation
from category.models import category,Sub_category
from django.views.decorators.cache import never_cache
from carts.models import CartItem,Carts
from carts.views import cart_id
from django.http import JsonResponse
from django.db.models import Q
import json

@never_cache
def store(request,category_slug=None):
    categories=None
    products=None
    print(category_slug)
   
    if category_slug !=None :
        print('1')
        category_slug = category_slug.strip()
        categories=get_object_or_404(category,slug=category_slug)
        #subcategory=Sub_category.objects.filter(categories=categories)
        products=Product.objects.all().filter(category=categories,is_available=True).order_by('id')
        product_count=products.count()
   
    else:    
        print('3')
    
        products=Product.objects.all().filter(is_available=True)        
        product_count=products.count()
   
    context= {
        'products':products,
        'product_count':product_count,
        
        
    }
    return render(request,('store/store.html'),context)
@never_cache
def Sub_product(request,category_id=None,subcategory_id=None):

    categories=get_object_or_404(category,id=category_id)
    sub_category=get_object_or_404(Sub_category,id=subcategory_id)
    products=Product.objects.filter(category=categories,subcategory=sub_category)
    product_count=products.count()    

    context= {
        'products':products,
        'product_count':product_count,
        
        
    }
    return render(request,('store/store.html'),context)



@never_cache
def product_detail(request,category_slug,Product_slug):
    
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=Product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=cart_id(request), product=single_product).exists()
        variation=Variation.objects.filter(product=single_product)
    except Exception as e:
        raise e
    
    unique_color=set()    
    unique_size={}
    for variation in single_product.variation_set.all():
        if variation.color.color_name not in unique_color:
            unique_color.add(variation.color.color_name)
            var_size=Variation.objects.filter(product=single_product,color=variation.color)
            size=set()
            for variation in var_size:
            #if variation.size.size not in unique_size:
                size.add(variation.size.size)   
            unique_size[variation.color.color_name]=list(size)   
    print(unique_size)             
            
    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'variation':variation,
        'unique_color':unique_color,
        'unique_size':unique_size,
        'sizesByColor': json.dumps(unique_size),
    }
    
    return render(request,'store/product_detail.html',context)


from django.http import JsonResponse

def get_variation_price(request):
    if request.method == 'GET':
        # Retrieve the product ID, color, and size from the request
        product_id = request.GET.get('product_id')
        color = request.GET.get('color')
        
        size = request.GET.get('size')
        

        try:
            # Find the matching variation based on color and size
            variation = Variation.objects.get(
                product_id=product_id,
                color__color_name=color,
                size__size=size
            )
            

            # Return the variation's price as a JSON response
            return JsonResponse({'price': variation.price})
        except Variation.DoesNotExist:
            # Handle the case where no matching variation is found
            return JsonResponse({'price': 0})
    else:
        # Handle other HTTP methods if necessary
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def search(request):
    if 'keyword' in request.GET:        
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()    
            context={
            'products':products,
            'product_count':product_count
                }  
            return render(request,('store/store.html'),context)
        else:
            return redirect(store)