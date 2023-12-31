from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from carts.models import CartItem, UserCoupons
from store.models import Product, com_offers
from .form import OrderForm
import datetime
from .models import Order, Payment, OrderProduct, order_details
import uuid
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# new
from django.views import View
from acounts.models import Adress, Wallet, Transaction
import json
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def payments(request, order_number):
    if request.method == "POST":
        payment_name = request.POST.get("payment_method")
        print(payment_name)
        if payment_name == "COD":
            order = Order.objects.get(
                user=request.user, is_ordered=False, order_number=order_number
            )
            unique_id = f"COD{order_number}"
            payment = Payment(
                user=request.user,
                payment_id=unique_id,
                payment_method=payment_name,
                amount_paid=0,
                status=payment_name,
            )
            payment.save()

        else:
            # Create a payment record
            body = json.loads(request.body)
            order = Order.objects.get(
                user=request.user, is_ordered=False, order_number=body["orderID"]
            )
            # order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
            payment = Payment(
                user=request.user,
                payment_id=body["transID"],
                payment_method=body["payment_method"],
                amount_paid=order.order_total,
                status=body["status"],
            )
            payment.save()

        order.payment = payment
        order.is_ordered = True
        order.status = "Accepted"
        order.save()
        print("payment")

        #  ove the cart items to the order product table
        cart_items = CartItem.objects.filter(user=request.user)
        for i in cart_items:
            print("name:", i.product.product_name)

        for item in cart_items:
            price = (
                item.variations.offer_price
                if item.variations.offer_price is not None
                else item.variations.price
            )
            orpr = OrderProduct()
            orpr.order_id = order.id
            orpr.payment = payment
            orpr.user_id = request.user.id
            orpr.product_id = item.product_id
            orpr.quantity = item.quantity
            orpr.product_price = price
            orpr.total = price * item.quantity
            orpr.ordered = True
            orpr.save()
            orderproduct = OrderProduct.objects.get(id=orpr.id)
            orderproduct.variations = item.variations
            orderproduct.save()

            # reduce quantity of the product
            product = Product.objects.get(id=item.product_id)
            variation = item.variations
            variation.stock -= item.quantity
            variation.save()
        CartItem.objects.filter(user=request.user).delete()

        mail_subject = "Thank you for your order"
        message = render_to_string(
            "orders/order_recieved_email.html", {"user": request.user, "order": order}
        )

        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        data = {
            "order_number": order.order_number,
            "transID": payment.payment_id,
        }
        if payment_name != "COD":
            print("olakka")
            return JsonResponse(data)
        else:
            transID = payment.payment_id
            redirect_url = "/orders/order_complete"
            query_string = f"?order_number={order_number}&payment_id={transID}"
            redirect_url_with_params = redirect_url + query_string

            # Redirect to the constructed URL
            return HttpResponseRedirect(redirect_url_with_params)


def place_order(request, total=0, quantity=0):
    # delete all unsuccessful orders
    unsuccessful_orders = Order.objects.all().exclude(
        Q(status="Cancelled") | Q(status="Completed")
    )
    unsuccessful_orders.delete()

    current_user = request.user
    # if the cart count is less than or equal to zero
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")
    original_total = 0
    total = 0
    grand_total = 0
    tax = 0
    price = 0
    user_coupon = None
    coupon_discount = 0
    discount_from_coupons = 0
    discount_from_offers = 0
    # here we will check any coupons applied still active
    try:
        user_coupon = UserCoupons.objects.get(
            user=request.user, applied=True, is_active=True
        )
    except:
        pass
    # if coupon aplly discount

    if user_coupon:
        coupon_discount = user_coupon.coupon.discount
    for cart_item in cart_items:
        if cart_item.variations.offer_price:
            price = cart_item.variations.offer_price
        else:
            price = cart_item.variations.price
        total += price * cart_item.quantity
        original_total += cart_item.variations.price * cart_item.quantity
        quantity += cart_item.quantity
    discount_from_coupons = (total * coupon_discount) / 100
    offer = original_total - total
    print("offer=", offer)
    print("total=", total)
    total = total - discount_from_coupons
    tax = (18 * total) / 100
    grand_total = total + tax

    # Retrieve the user's saved addresses
    saved_addresses = Adress.objects.filter(user=current_user)

    if request.method == "POST":
        # fetch the adress selected

        selected_address_id = request.POST.get("selected_address")
        try:
            sel_offer = request.POST.get("selected_offer")
        except:
            pass
        try:
            c_offer = com_offers.objects.get(id=sel_offer)
        except com_offers.DoesNotExist:
            pass

        if selected_address_id != "new":
            try:
                selected_address = Adress.objects.get(pk=selected_address_id)
            except:
                messages.error(
                    request,
                    "Please choose an adress to place order",
                    extra_tags="address-error",
                )
                return redirect("checkout")

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
                ip=request.META.get("REMOTE_ADDR"),
                # here com offers
            )
            # generate order number
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(order1.id)
            order1.order_number = order_number
            order1.save()
            order_det = order_details.objects.create(
                order=order1,
                original_total=original_total,
                discount_from_coupons=discount_from_coupons,
                discount_from_offers=discount_from_offers,
                sub_total=total,
                tax=tax,
                grand_total=grand_total,
            )
            try:
                if c_offer:
                    # check if offer exceeds maxium discount
                    mx_discount = c_offer.maximum_discount
                    order1.offers = c_offer
                    discount_from_offer = original_total * (c_offer.discount / 100)
                    if discount_from_offer > mx_discount:
                        discount_from_offer = mx_discount
                    discount_from_offers = discount_from_offer + offer
                    total = total - discount_from_offer
                    tax = total * (18 / 100)
                    grand_total = total + tax
                    order_det.discount_from_coupons = discount_from_coupons
                    order_det.discount_from_offers = discount_from_offers
                    order_det.sub_total = total
                    order_det.tax = tax
                    order_det.grand_total = grand_total
                    order_det.save()
                    order1.order_total = grand_total
                    order1.tax = tax
                    order1.save()
            except:
                pass
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number
            )

        else:
            form = OrderForm(request.POST)
            # save the adress if
            selected_adress = request.POST.get("selected_address")
            if selected_adress == "new":
                print("get o")
                user = request.user
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                full_name = f"{first_name} {last_name}"
                phone_number = request.POST.get("phone_number")
                adress_line1 = request.POST.get("adress_line1")
                adress_line2 = request.POST.get("adress_line2")
                city = request.POST.get("city")
                state = request.POST.get("state")
                country = request.POST.get("country")
                pincode = request.POST.get("pin")
                adress = Adress(
                    user=user,
                    name=full_name,
                    phone_number=phone_number,
                    adress_line1=adress_line1,
                    adress_line2=adress_line2,
                    city=city,
                    state=state,
                    country=country,
                    pin=pincode,
                )
                adress.save()

            # upto here
            if form.is_valid():
                # store all the billing information inside order table
                data = Order()
                data.user = current_user
                data.first_name = form.cleaned_data["first_name"]
                data.last_name = form.cleaned_data["last_name"]
                data.phone_number = form.cleaned_data["phone_number"]
                data.email = form.cleaned_data["email"]
                data.adress_line1 = form.cleaned_data["adress_line1"]
                data.adress_line2 = form.cleaned_data["adress_line2"]
                data.country = form.cleaned_data["country"]
                data.state = form.cleaned_data["state"]
                data.city = form.cleaned_data["city"]
                data.order_note = form.cleaned_data["order_note"]
                data.order_total = grand_total
                data.pin = form.cleaned_data["pin"]
                data.tax = tax
                data_ip = request.META.get("REMOTE_ADDR")
                data.save()
                # generate order number
                yr = int(datetime.date.today().strftime("%Y"))
                dt = int(datetime.date.today().strftime("%d"))
                mt = int(datetime.date.today().strftime("%m"))
                d = datetime.date(yr, mt, dt)
                current_date = d.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
                order_det = order_details.objects.create(
                    order=data,
                    original_total=original_total,
                    discount_from_coupons=discount_from_coupons,
                    discount_from_offers=discount_from_offers,
                    sub_total=total,
                    tax=tax,
                    grand_total=grand_total,
                )
                try:
                    if c_offer:
                        data.offers = c_offer
                        mx_discount = c_offer.maximum_discount
                        discount_from_offer = total * (c_offer.discount / 100)
                        discount_from_offers = discount_from_offer + offer
                        if discount_from_offer > mx_discount:
                            discount_from_offer = mx_discount
                        total = total - discount_from_offer
                        tax = total * (18 / 100)
                        grand_total = total + tax
                        order_det.discount_from_coupons = discount_from_coupons
                        order_det.discount_from_offers = discount_from_offers
                        order_det.sub_total = total
                        order_det.tax = tax
                        order_det.grand_total = grand_total
                        order_det.save()
                        data.order_total = grand_total
                        data.tax = tax
                        data.save()
                except:
                    pass
                order = Order.objects.get(
                    user=current_user, is_ordered=False, order_number=order_number
                )

            else:
                form = OrderForm()
                print(form.errors)

        print("you are here")
        total = round(total, 2)
        tax = round(tax, 2)
        grand_total = round(grand_total, 2)
        context = {
            "saved_addresses": saved_addresses,
            "order": order,
            "cart_items": cart_items,
            "total": total,
            "tax": tax,
            "grand_total": float(grand_total),
        }
        print(order.order_number)
        return render(request, "orders/payments.html", context)

    else:
        return redirect("checkout")


def cancel_order(request, order_number):
    try:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    except:
        if request.user.is_admin:
            order = order = get_object_or_404(Order, order_number=order_number)
    payment = order.payment
    orpr = OrderProduct.objects.filter(order=order, payment=payment)
    if request.method == "POST":
        if order.is_ordered:
            orderproducts = OrderProduct.objects.filter(order=order)
            for or_product in orderproducts:
                product = or_product.product
                variation = or_product.variations
                variation.stock += or_product.quantity
                variation.save()
            order.is_ordered = False
            order.status = "Cancelled"
            order.save()
        if payment:
            payment.status = "Cancelled"
            payment.save()
        if orpr:
            for i in orpr:
                i.ordered = False
                i.save()
            if request.user.is_admin:
                return redirect("orders")
        try:
            order.reason_for_cancellation = request.POST.get("reason")
            order.save()
        except Order.DoesNotExist:
            pass

        # here wallet
        try:
            wallet = Wallet.objects.get(user=request.user)
            if order.status == "Cancelled" and payment.payment_method == "PayPal":
                amount = order.order_total
                wallet.add_fund(amount)
                description = f"Refund for order #{order.order_number}"
                transaction = Transaction(
                    wallet=wallet,
                    amount=amount,
                    description=description,
                    balance=wallet.balance,
                )
                transaction.save()
        except Wallet.DoesNotExist:
            pass
            return redirect("user_dashboard")
    if request.user.is_admin:
        return redirect("orders")
    return redirect("user_dashboard")


def order_complete(request):
    order_number = request.GET.get("order_number")
    transID = request.GET.get("payment_id")
    # make coupon invalid
    order = Order.objects.get(order_number=order_number)
    try:
        user_coupon = UserCoupons.objects.get(
            user=request.user, applied=True, is_active=True
        )
        if order.is_ordered == True:
            user_coupon.is_active = False
            user_coupon.save()
    except:
        pass

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        order.status = "Completed"
        order.save()
        order_products = OrderProduct.objects.filter(order_id=order.id)
        total = 0
        # order deatils
        ord_det = order_details.objects.get(order=order)
        ord_det.status = True
        ord_det.save()
        for op in order_products:
            price = (
                op.variations.offer_price
                if op.variations.offer_price
                else op.variations.price
            )
            total += price * op.quantity
        payment = Payment.objects.get(payment_id=transID)
        subtotal = order.order_total - order.tax
        subtotal = round(subtotal, 2)
        # to find offer from offers only
        cat_offer = ord_det.original_total - total
        discount = (
            ord_det.discount_from_coupons + ord_det.discount_from_offers - cat_offer
        )
        discount = round(discount, 2)

        context = {
            "order": order,
            "order_products": order_products,
            "transID": payment.payment_id,
            "payment": payment,
            "subtotal": subtotal,
            "total": total,
            "discount": discount,
            "ord_det": ord_det,
        }
        return render(request, "orders/order_confirmation.html", context)
    except (Payment.DoesNotExist, Order.DoesNotexist):
        return redirect("home")


# render to pdf
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


# Opens up page as PDF


class ViewPDF(View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        ord_det = order_details.objects.get(order=order)
        payment = order.payment
        order_products = OrderProduct.objects.filter(order=order)
        grand_total = order.order_total
        # find irdr det
        total = 0
        for op in order_products:
            price = (
                op.variations.offer_price
                if op.variations.offer_price
                else op.variations.price
            )
            total += price * op.quantity
        cat_offer = ord_det.original_total - total
        discount = (
            ord_det.discount_from_coupons + ord_det.discount_from_offers - cat_offer
        )
        data = {
            "invoice_number": order.order_number,
            "invoice_date": payment.created_at,
            "customer_name": order.full_name,
            "total": total,
            "items": order_products,
            "order_total": order.order_total,
            "tax": order.tax,
            "grand_total": grand_total,
            "ord_det": ord_det,
            "order": order,
            "discount": discount,
        }
        pdf = render_to_pdf("orders/invoice.html", data)
        return HttpResponse(pdf, content_type="application/pdf")


class DownloadPDF(View):
    def get(self, request, order_id, *args, **kwargs):
        # Fetch the order and related data
        order = Order.objects.get(id=order_id)
        payment = order.payment
        order_products = OrderProduct.objects.filter(order=order)
        grand_total = order.order_total

        # Prepare data for the PDF template
        data = {
            "invoice_number": order.order_number,
            "invoice_date": payment.created_at,
            "customer_name": order.full_name,
            "total_amount": payment.amount_paid,
            "items": order_products,
            "order_total": order.order_total,
            "tax": order.tax,
            "grand_total": grand_total,
        }

        # Render the PDF using your render_to_pdf function
        pdf = render_to_pdf("orders/invoice.html", data)

        # Create an HTTP response with the PDF content
        response = HttpResponse(pdf.getvalue(), content_type="application/pdf")

        # Set the Content-Disposition header to suggest a filename
        filename = "Invoice_%s.pdf" % order.order_number
        content = f"attachment; filename='{filename}'"
        response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'

        return response


def generate_invoice_pdf(request, order_id):
    # Get invoice data (replace with your data retrieval logic)
    order = Order.objects.get(id=order_id)
    ord_det = order_details.objects.get(order=order)
    payment = order.payment
    order_products = OrderProduct.objects.filter(order=order)
    grand_total = order.order_total
    # find irdr det
    total = 0
    for op in order_products:
        price = (
            op.variations.offer_price
            if op.variations.offer_price
            else op.variations.price
        )
    total += price * op.quantity
    cat_offer = ord_det.original_total - total
    discount = ord_det.discount_from_coupons + ord_det.discount_from_offers - cat_offer
    invoice_data = {
        "invoice_number": order.order_number,
        "invoice_date": payment.created_at,
        "customer_name": order.full_name,
        "total": total,
        "items": order_products,
        "order_total": order.order_total,
        "tax": order.tax,
        "grand_total": grand_total,
        "ord_det": ord_det,
        "order": order,
        "discount": discount,
    }

    # Render the HTML template with data
    template = get_template("orders/invoice.html")
    html = template.render(invoice_data)

    # Enable logging
    pisa.showLogging()

    # Create a PDF response
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    # pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf)

    response = HttpResponse(pdf.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'
    return response
