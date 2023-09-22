from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse,get_object_or_404
from django.http import JsonResponse
from carts.models import CartItem
from store.models import Product
from .form import OrderForm
import datetime
from.models import Order,Payment,OrderProduct
import uuid
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
#new 
from acounts.models import Adress
import json
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# Create your views here.
def payments(request,order_number):
    # Create a payment record
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    #order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status']               
    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    print("payment")
     #  ove the cart items to the order product table
    cart_items=CartItem.objects.filter(user=request.user)
    for i in cart_items:
        print ("name:",i.product.product_name)
    for item in cart_items:
        orpr=OrderProduct()
        orpr.order_id=order.id
        orpr.payment=payment
        orpr.user_id=request.user.id
        orpr.product_id=item.product_id
        orpr.quantity=item.quantity        
        orpr.product_price=item.variations.price
        orpr.total=item.variations.price*item.quantity
        orpr.ordered=True
        
        orpr.save()
        #cart_item=CartItem.objects.get(id=item.id)
        #product_variation=cart_item.variations
        orderproduct=OrderProduct.objects.get(id=orpr.id)
        orderproduct.variations=item.variations
        orderproduct.save()
        # reduce quantity of the product
        product=Product.objects.get(id=item.product_id)
        #product.stock -=item.quantity
        variation=item.variations
        print("stch",variation.stock)
        variation.stock -=item.quantity
        #product.save()
        variation.save()    
    CartItem.objects.filter(user=request.user).delete()    
    
    mail_subject='Thank you for your order'
    message=render_to_string('orders/order_recieved_email.html',{
                                        'user':request.user,
                                      'order':order
                                    })                               
                                      
    to_email=request.user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    
    data={
        'order_number':order.order_number,
        'transID':payment.payment_id,
        
    }
    return JsonResponse(data)
    
    
    return render(request,'orders/order_confirmation.html') 
   

def place_order(request,total=0,quantity=0):
    current_user=request.user
    # if the cart count is less than or equal to zero 
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count <=0:
        return redirect('store')
    
    grand_total=0
    tax=0
    for cart_item in cart_items:
        total += (cart_item.variations.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax    
    
     # Retrieve the user's saved addresses
    saved_addresses = Adress.objects.filter(user=current_user)
    
    if request.method=='POST':
        print('ok')
        #new
        selected_address_id = request.POST.get('selected_address')

        if selected_address_id !='new' :
            print('ok2')
            # User selected a saved address
            selected_address = Adress.objects.get(pk=selected_address_id)

            # Create an order record with the selected address
            order1 = Order.objects.create(
                user=current_user,
                first_name=selected_address.name,
                pin=selected_address.pin,
                phone_number=selected_address.phone_number,
                email=selected_address.email,
                adress_line1=selected_address.adress_line1,
                adress_line2=selected_address.adress_line2,
                country=selected_address.country,
                state=selected_address.state,
                city=selected_address.city,
                  # Include order note
                order_total=grand_total,
                tax=tax,
                ip=request.META.get('REMOTE_ADDR'),
                
            )
       
                # generate order number
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime('%Y%m%d')
            order_number=current_date+str(order1.id)
            order1.order_number=order_number
            order1.save()
            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)     
            
        else:  
            form=OrderForm(request.POST)            
            if form.is_valid():
                print('form is valid')
                # store all the billing information inside order table 
                data=Order()
                data.user=current_user
                data.first_name=form.cleaned_data['first_name']
                data.last_name=form.cleaned_data['last_name']
                data.phone_number=form.cleaned_data['phone_number']
                data.email=form.cleaned_data['email']
                data.adress_line1=form.cleaned_data['adress_line1']
                data.adress_line2=form.cleaned_data['adress_line2']
                data.country=form.cleaned_data['country']
                data.state=form.cleaned_data['state']
                data.city=form.cleaned_data['city']
                data.order_note=form.cleaned_data['order_note']
                data.order_total=grand_total
                data.pin=form.cleaned_data['pin']
                data.tax=tax
                data_ip=request.META.get('REMOTE_ADDR')
                data.save()
                # generate order number
                yr=int(datetime.date.today().strftime('%Y'))
                dt=int(datetime.date.today().strftime('%d'))
                mt=int(datetime.date.today().strftime('%m'))
                d=datetime.date(yr,mt,dt)
                current_date=d.strftime('%Y%m%d')
                order_number=current_date+str(data.id)
                data.order_number=order_number
                data.save()
                order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            else:                
                form=OrderForm()    
                print(form.errors)    
               
        print('you are here')        
        context={
                    'saved_addresses': saved_addresses,
                    'order':order,
                    'cart_items':cart_items,
                    'total':total,
                    'tax':tax,
                    'grand_total':grand_total
                }
        print(order.order_number)
        return render(request,'orders/payments.html',context)
    
    else:
        return redirect('checkout')    
    
    
def cancel_order(request,order_number):
    print('1')  
    print(order_number)
    order=get_object_or_404(Order,order_number=order_number,user=request.user)
    payment=order.payment
    orpr=OrderProduct.objects.filter(order=order,payment=payment)
    print(order)
    if request.method=='POST':
        print('2')  
        if order.is_ordered:
            print('3')  
            orderproducts=OrderProduct.objects.filter(order=order)
            for or_product in orderproducts:
                product=or_product.product
                variation=or_product.variations
                variation.stock += or_product.quantity
                variation.save()
            order.is_ordered=False
            order.save()  
        if payment:
            payment.status='Cancelled' 
            payment.save()
        if orpr:
            for i in orpr:
                i.ordered=False
                i.save()       
            
            print('its ok')  
            return redirect('user_dashboard')
                
    return redirect('user_dashboard')    

def order_complete(request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
    
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        order_products=OrderProduct.objects.filter(order_id=order.id)
        for i in order_products:
            print("yes",i.product.product_name)
        payment=Payment.objects.get(payment_id=transID)
        subtotal=0
        for i in order_products:
            subtotal +=i.variations.price*i.quantity
        context={
            'order':order,
            'order_products':order_products,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal
        }
        return render(request,'orders/order_confirmation.html',context)
    except (Payment.DoesNotExist , Order.DoedNotexist):
        return redirect('home')
    

# weasy print generate pdf

# views.py


def generate_invoice_pdf(request,order_id):
    # Get invoice data (replace with your data retrieval logic)
    order=Order.objects.get(id=order_id)
    payment=order.payment
    order_products=OrderProduct.objects.filter(order=order)

    grand_total=order.order_total+order.tax
    invoice_data = {
        'invoice_number': order.order_number,
        'invoice_date': payment.created_at,
        'customer_name': order.full_name,      
        'total_amount': payment.amount_paid,
        'items':order_products,        
        'order_total':order.order_total,
        'tax':order.tax,
        'grand_total':grand_total
    }

    # Render the HTML template with data
    template = get_template('orders/invoice.html')
    html = template.render(invoice_data)

    # Create a PDF response
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf)

    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response


        
    

    
    

            
            
            
            
    
  