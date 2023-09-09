from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse,get_object_or_404
from acounts.models import Acount
from store.models import Product,softdelete,NonDeleted
from category.models import category
from.form import ProductForm
from django.db.models import Q
from django.contrib import messages


def ad_dashboard(request):
    users=Acount.objects.all()
    context={
        'users':users
    }
    
  
    return render(request,'admins/dashboard.html',context)


def customers(request):
    customers=Acount.objects.all().order_by('date_joined')
    context={
        'customers':customers        
    }   
    return render(request,'admins/customers.html',context)

def block_unblock_user(request,user_id):   
    user = get_object_or_404(Acount, id=user_id)
    action = request.POST.get('action')

    if action == 'block':
        user.is_active = False
    elif action == 'unblock':
        user.is_active = True

    user.save()
    return redirect('customers')

def delete_customer(request,user_id):
    try:
        user=Acount.objects.get(id=user_id)
        user.delete()
        return redirect('customers')
    except Acount.DoesNotExist:
         return redirect('customers')
def ad_products(request):
    
    products=Product.objects.all().order_by('created_date')
    categories=category.objects.all()
    context={
        'products':products,
        'categories':categories
    }    
    return render(request,'admins/products.html',context)  

def add_products(request):
    
    if request.method == 'POST':
        product_name    = request.POST.get('product_name')
        slug            = request.POST.get('slug')
        
        existing_product=Product.objects.filter(Q(product_name=product_name) | Q(slug=slug)).first()
        
        if existing_product:
             messages.error(request, "Product with this name or slug already exists.")
            
        else:    
            
            description     = request.POST.get('description')
            price           = request.POST.get('price')
            image_file      = request.FILES.get('images')
            stock           = request.POST.get('stock')
            is_available    = request.POST.get('is_available')
            category_id      = request.POST.get('category')
            created_date    = request.POST.get('created_date')
            modified_date   = request.POST.get('modified_date')
            
            product=Product(
            product_name    = product_name,
            slug            = slug,
            description     = description,
            price           = price,
            images          = image_file,
            stock           = stock,
            is_available    = is_available,
            category_id     = category_id,
            created_date    = created_date,
            modified_date   = modified_date
            )    
            
            product.save()
            messages.success(request, "Product added successfully.")
        return redirect('ad_products')
        
def edit_products(request,product_id):
        
    if request.method == 'POST': 
        product_name    = request.POST.get('product_name')
        slug            = request.POST.get('slug')
        existing_product=Product.objects.filter(Q(product_name=product_name) | Q(slug=slug)).exclude(pk=product_id).first()
        if existing_product:
            messages.error(request, "Product with this name or slug already exists.")
        else: 
            product=Product.objects.get(id=product_id)
            if 'images' in request.FILES:
                    product.images=request.FILES.get('images') 
            product.product_name    = request.POST.get('product_name')
            product.slug            = request.POST.get('slug')
            product.description     = request.POST.get('description')
            product.price           = request.POST.get('price')        
            product.stock           = request.POST.get('stock')
            product.is_available    = request.POST.get('is_available')
            product.category_id     = request.POST.get('category')    
            product.modified_date   = request.POST.get('modified_date')
                
            
            
            product.save()
            messages.success(request,"Prduct details updated successfully")
       
    return redirect('ad_products')   

def delete_products(request,product_id):
    try:
        product=Product.objects.get(id=product_id)
        product.SoftDelete()
        return redirect('ad_products')
    except Product.DoesNotExist:
        return redirect('ad_products')
    
    
def ad_category(request):
    categories=category.objects.all().order_by('id')
    context={
        'categories':categories
    }
    return render(request,'admins/category.html',context)    
def add_category(request):
    
    if request.method == 'POST':
        category_name    = request.POST.get('category_name')
        slug            = request.POST.get('slug')
        
        existing_category=category.objects.filter(Q(category_name=category_name) | Q(slug=slug)).first()
        
        if existing_category:
             messages.error(request, "Category with this name or slug already exists.")
            
        else:   
            description=request.POST.get('description')
            image=request.FILES.get('images')
            
            new_category=category(
                
                category_name=category_name,
                slug=slug,
                cat_image=image,
                description=description             
             )
            new_category.save()
            messages.success(request,"New category is succesfully added")
    return redirect('ad_category')        
                
def edit_category(request,cat_id):
    if request.method == 'POST':
        up_category_name        =request.POST.get('category_name')
        up_slug_name            =request.POST.get('slug')
        existing_category_name  =category.objects.filter(category_name=up_category_name).exclude(pk=cat_id).first()
        existing_category_slug  =category.objects.filter(slug=up_slug_name).exclude(pk=cat_id).first()
        if existing_category_name:
            messages.error(request,"Category name already exists")
        elif existing_category_slug:
            messages.error("Category slug already exists")    
        else:
            cat=category.objects.get(id=cat_id)
            if 'images' in request.FILES:
                cat.cat_image=request.FILES.get('images')
            
            cat.category_name=up_category_name
            cat.slug=up_slug_name
            cat.description=request.POST.get('description')
            
            cat.save()
            messages.success(request,"Category updated succesfully")
    
    return redirect('ad_category')   


def delete_category(request,cat_id):
    try:
        cat=category.objects.get(id=cat_id)
        cat.delete()
        return redirect('ad_category')
    except category.DoesNotExist:
        return redirect('ad_category')
        

     
                
                     
            
                
      

            
    
        
  
    
    

# Create your views here.
