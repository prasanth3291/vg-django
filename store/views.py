from django.shortcuts import render,get_object_or_404,redirect
from.models import Product
from category.models import category
from django.views.decorators.cache import never_cache
from carts.models import CartItem,Carts
from carts.views import cart_id
from django.db.models import Q

@never_cache
def store(request,category_slug=None):
    categories=None
    products=None
    
    if category_slug !=None:
        category_slug = category_slug.strip()
        categories=get_object_or_404(category,slug=category_slug)
        products=Product.objects.all().filter(category=categories,is_available=True).order_by('id')
        product_count=products.count()
    else:    
    
        products=Product.objects.all().filter(is_available=True)        
        product_count=products.count()
        
        
    context= {
        'products':products,
        'product_count':product_count
    }
    return render(request,('store/store.html'),context)

@never_cache
def product_detail(request,category_slug,Product_slug):  
  
    
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=Product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    context={
        'single_product':single_product,
        'in_cart':in_cart
    }
    
    return render(request,'store/product_detail.html',context)


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