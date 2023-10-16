from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, get_object_or_404
from acounts.models import Acount, Coupons, UserProfile, Referal_code
from store.models import (
    Product,
    softdelete,
    NonDeleted,
    Offer,
    com_offers,
    Discount,
    Variation,
    Sub_category,
)
from category.models import category
from .form import ProductForm, CouponsForm, CategoryOfferForm, Minimum_purchaseOfferForm
from django.db.models import Q, Count, Sum, F
from django.contrib import messages
from orders.models import Order, OrderProduct, Payment, order_details
from carts.models import UserCoupons
import json
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


def ad_dashboard(request):
    try:
        completed_orders_by_category = category.objects.annotate(
            completed_order_count=Sum(
                F("product__variation__orderproduct__quantity"),
                filter=Q(product__variation__orderproduct__order__status="Completed"),
            )
        )
    except:
        pass
    category_name = []
    category_count = []
    try:
        for categor in completed_orders_by_category:
            if categor.completed_order_count is not None:
                category_name.append(categor.category_name)
                category_count.append(float(categor.completed_order_count))
    except:
        pass

    category_name_json = json.dumps(category_name)
    category_count_json = json.dumps(category_count)
    # fine transacxtion details
    # Filter completed orders
    completed_orders = Order.objects.filter(status="Completed")

    # Count payment methods used in completed orders
    completed_transaction_by_payment = completed_orders.values(
        "payment__payment_method"
    ).annotate(method_count=Count("payment__payment_method"))
    transaction_type = []
    transaction_count = []
    for item in completed_transaction_by_payment:
        if item["payment__payment_method"] is not None:
            transaction_type.append(item["payment__payment_method"])
            transaction_count.append(int(item["method_count"]))
    transaction_type_json = json.dumps(transaction_type)
    transaction_count_json = json.dumps(transaction_count)
    # find  orders by date
    orders_growth = (
        Order.objects.annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count_by_date=Count("id"))
        .order_by("date")
    )
    order_date = []
    order_count = []
    for item in orders_growth:
        order_date.append(str(item["date"]))
        order_count.append((item["count_by_date"]))

    order_date_json = json.dumps(order_date)
    order_count_json = json.dumps(order_count)

    # today sale
    current_datetime = timezone.now()
    start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = current_datetime.replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    today_sales = (
        Order.objects.filter(created_at__range=(start_of_day, end_of_day)).aggregate(
            total_sales=Sum("order_total")
        )["total_sales"]
        or 0
    )

    # total sale
    total_sales = Order.objects.all().aggregate(total_Sales=Sum("order_total"))
    total_sales = total_sales["total_Sales"]
    # todays orders
    today_orders = (
        Order.objects.filter(
            created_at__range=(start_of_day, end_of_day), status="Completed"
        ).aggregate(todays_order_count=Count("order_number"))["todays_order_count"]
        or 0
    )

    # total orders
    total_orders = (
        Order.objects.filter(Q(status="Completed") | Q(status="Cancelled")).aggregate(
            total_orders=Count("order_number")
        )["total_orders"]
        or 0
    )

    # order table for payment
    orders = Order.objects.filter(status="Completed").order_by("-created_at")[:5]
    return render(
        request,
        "admins/dashboard.html",
        {
            "category_name_json": category_name_json,
            "category_count_json": category_count_json,
            "transaction_type_json": transaction_type_json,
            "transaction_count_json": transaction_count_json,
            "order_date_json": order_date_json,
            "order_count_json": order_count_json,
            "orders": orders,
            "today_sales": today_sales,
            "total_sales": total_sales,
            "today_orders": today_orders,
            "total_orders": total_orders,
        },
    )


def customers(request):
    customers = Acount.objects.all().order_by("date_joined")
    context = {"customers": customers}
    return render(request, "admins/customers.html", context)


def block_unblock_user(request, user_id):
    user = get_object_or_404(Acount, id=user_id)
    action = request.POST.get("action")

    if action == "block":
        user.is_active = False
    elif action == "unblock":
        user.is_active = True

    user.save()
    return redirect("customers")


def delete_customer(request, user_id):
    try:
        user = Acount.objects.get(id=user_id)
        user.delete()
        return redirect("customers")
    except Acount.DoesNotExist:
        return redirect("customers")


def ad_products(request):
    products = Product.objects.all().order_by("created_date")
    categories = category.objects.all()
    subcategories = Sub_category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "subcategories": subcategories,
    }
    return render(request, "admins/products.html", context)


def add_products(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        slug = request.POST.get("slug")
        existing_product = Product.objects.filter(
            Q(product_name=product_name) | Q(slug=slug)
        ).first()
        if existing_product:
            messages.error(request, "Product with this name or slug already exists.")
        else:
            description = request.POST.get("description")
            image_file = request.FILES.get("images")
            is_available = request.POST.get("is_available")
            category_id = request.POST.get("category")
            created_date = request.POST.get("created_date")
            modified_date = request.POST.get("modified_date")
            subcategory_id = request.POST.get("subcategory")

            product = Product(
                product_name=product_name,
                slug=slug,
                description=description,
                images=image_file,
                is_available=is_available,
                category_id=category_id,
                created_date=created_date,
                modified_date=modified_date,
                subcategory_id=subcategory_id,
            )
            product.save()
            messages.success(request, "Product added successfully.")
        return redirect("ad_products")


def edit_products(request, product_id):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        slug = request.POST.get("slug")
        existing_product = (
            Product.objects.filter(Q(product_name=product_name) | Q(slug=slug))
            .exclude(pk=product_id)
            .first()
        )
        if existing_product:
            messages.error(request, "Product with this name or slug already exists.")
        else:
            product = Product.objects.get(id=product_id)
            if "images" in request.FILES:
                product.images = request.FILES.get("images")
            product.product_name = request.POST.get("product_name")
            product.slug = request.POST.get("slug")
            product.description = request.POST.get("description")
            product.is_available = request.POST.get("is_available")
            product.category_id = request.POST.get("category")
            product.modified_date = request.POST.get("modified_date")
            product.subcategory_id = request.POST.get("subcategory")
            product.save()
            messages.success(request, "Product details updated successfully")
    return redirect("ad_products")


def delete_products(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.SoftDelete()
        return redirect("ad_products")
    except Product.DoesNotExist:
        return redirect("ad_products")


def ad_category(request):
    categories = category.objects.all().order_by("id")
    context = {"categories": categories}
    return render(request, "admins/category.html", context)


def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        slug = request.POST.get("slug")
        existing_category = category.objects.filter(
            Q(category_name=category_name) | Q(slug=slug)
        ).first()
        if existing_category:
            messages.error(request, "Category with this name or slug already exists.")
        else:
            description = request.POST.get("description")
            image = request.FILES.get("images")
            new_category = category(
                category_name=category_name,
                slug=slug,
                cat_image=image,
                description=description,
            )
            new_category.save()
            messages.success(request, "New category is succesfully added")
    return redirect("ad_category")


def edit_category(request, cat_id):
    if request.method == "POST":
        up_category_name = request.POST.get("category_name")
        up_slug_name = request.POST.get("slug")
        existing_category_name = (
            category.objects.filter(category_name=up_category_name)
            .exclude(pk=cat_id)
            .first()
        )
        existing_category_slug = (
            category.objects.filter(slug=up_slug_name).exclude(pk=cat_id).first()
        )
        if existing_category_name:
            messages.error(request, "Category name already exists")
        elif existing_category_slug:
            messages.error("Category slug already exists")
        else:
            cat = category.objects.get(id=cat_id)
            if "images" in request.FILES:
                cat.cat_image = request.FILES.get("images")
            cat.category_name = up_category_name
            cat.slug = up_slug_name
            cat.description = request.POST.get("description")
            cat.save()
            messages.success(request, "Category updated succesfully")
    return redirect("ad_category")


def delete_category(request, cat_id):
    try:
        cat = category.objects.get(id=cat_id)
        cat.delete()
        return redirect("ad_category")
    except category.DoesNotExist:
        return redirect("ad_category")


def orders(request):
    orders = Order.objects.all().order_by("-created_at")
    context = {"orders": orders}
    return render(request, "admins/orders.html", context)


def order_details_admin(request, order_id):
    order = Order.objects.get(id=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    print(order_products)
    context = {"order": order, "order_products": order_products}
    return render(request, "admins/order_details_admin.html", context)


def coupons(request):
    coupons = Coupons.objects.all()
    context = {"coupons": coupons}
    return render(request, "admins/coupons.html", context)


def add_coupons(request):
    if request.method == "POST":
        name = request.POST.get("name")
        discount = request.POST.get("discount")
        valid_from = request.POST.get("valid_from")
        valid_to = request.POST.get("valid_to")
        coupon_count = request.POST.get("coupon_count")
        minimum_amount = request.POST.get("minimum_amount")
        maximum_discount = request.POST.get("maximum_discount")
        status = request.POST.get("status")

        # Create a new coupon object with the form data
        coupon = Coupons(
            name=name,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
            coupon_count=coupon_count,
            minimum_amount=minimum_amount,
            maximum_discount=maximum_discount,
            status=(status == "on"),  # Convert 'on' to True for checkbox value
        )
        coupon.save()
        return redirect("coupons")
    return render(request, "admins/add_coupons.html")


def edit_coupons(request, coupon_id):
    coupon = get_object_or_404(Coupons, id=coupon_id)
    coupon_form = None
    if request.method == "POST":
        coupon_form = CouponsForm(request.POST, instance=coupon)
        if coupon_form.is_valid():
            coupon_form.save()
            # Redirect or do something else after successful form submission
            return redirect("coupons")
    else:
        coupon_form = CouponsForm(
            instance=coupon
        )  # Initialize form with the coupon instance

    context = {"coupon_form": coupon_form, "coupon": coupon}

    context = {"coupon_form": coupon_form, "coupon": coupon}

    return render(request, "admins/edit_coupons.html", context)


def delete_coupons(request, coupon_id):
    try:
        coupon = Coupons.objects.get(id=coupon_id)
        coupon.delete()
    except:
        pass
    return redirect("coupons")


def profiles(request, customer_id):
    us = Acount.objects.get(id=customer_id)
    user = None
    try:
        user = UserProfile.objects.get(user=us)
        context = {"user": user}
        return render(request, "admins/profiles.html", context)
    except:
        user = None
        context = {"user": user}
        return render(request, "admins/profiles.html", context)


def ad_refer(request):
    codes = Referal_code.objects.all()
    return render(request, "admins/admin-refer.html", {"codes": codes})


def category_offers(request):
    cat_offers = Offer.objects.all()
    context = {"cat_offers": cat_offers}
    return render(request, "admins/category-offers.html", context)


def minimum_purchase_offers(request):
    com_offer = com_offers.objects.all()
    context = {"com_offers": com_offer}
    return render(request, "admins/minimum-purchase-offers.html", context)


def add_category_offer(request):
    discounts = Discount.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        discount = request.POST.get("discount")
        start_date = request.POST.get("valid_from")
        end_date = request.POST.get("valid_to")
        description = request.POST.get("description")
        # create new offer
        Offer.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            discount_id=discount,
        )

        return redirect("category_offers")

    context = {"discounts": discounts}

    return render(request, "admins/add_category_offer.html", context)


def edit_category_offer(request, offer_id):
    offers = Offer.objects.get(id=offer_id)
    if request.method == "POST":
        offer_form = CategoryOfferForm(request.POST, instance=offers)
        offer_form.save()
        context = {"offer": offers, "offer_form": offer_form}
        return redirect("category_offers")
    else:
        offer_form = CategoryOfferForm(instance=offers)
        context = {"offer": offers, "offer_form": offer_form}
        return render(request, "admins/edit_category_offers.html", context)


def delete_category_offer(request, offer_id):
    category_offer = Offer.objects.get(id=offer_id)
    category_offer.delete()
    return redirect("category_offers")


def add_minimum_purchase_offer(request):
    if request.method == "POST":
        name = request.POST.get("name")
        discount = request.POST.get("discount")
        start_date = request.POST.get("valid_from")
        end_date = request.POST.get("valid_to")
        description = request.POST.get("description")
        minimum_value = request.POST.get("minimum_value")
        maximum_discount = request.POST.get("maximum_discount")
        # create new offer
        com_offers.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            discount=discount,
            mimimum_value=minimum_value,
            maximum_discount=maximum_discount,
        )

        return redirect("minimum_purchase_offers")
    return render(request, "admins/add_minimum_purchase_offer.html")


def edit_minimum_purchase_offer(request, offer_id):
    offers = com_offers.objects.get(id=offer_id)
    if request.method == "POST":
        offer_form = Minimum_purchaseOfferForm(request.POST, instance=offers)
        offer_form.save()
        context = {"offer": offers, "offer_form": offer_form}
        return redirect("minimum_purchase_offers")
    else:
        offer_form = Minimum_purchaseOfferForm(instance=offers)
        context = {"offer": offers, "offer_form": offer_form}
        return render(request, "admins/edit_minimum_purchase_offer.html", context)


def delete_minimum_purchase_offer(request, offer_id):
    category_offer = com_offers.objects.get(id=offer_id)
    category_offer.delete()
    return redirect("minimum_purchase_offers")


def sales_report(request):
    orders = Order.objects.filter(Q(status="Completed") | Q(status="Cancelled"))
    order_products = OrderProduct.objects.filter(order__in=orders)
    order_detail = order_details.objects.all()
    order_detail = order_detail.annotate(
        total_discount=F("discount_from_offers") + F("discount_from_coupons")
    )
    # today sale
    current_datetime = timezone.now()
    start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = current_datetime.replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    today_sales = (
        Order.objects.filter(created_at__range=(start_of_day, end_of_day)).aggregate(
            total_sales=Sum("order_total")
        )["total_sales"]
        or 0
    )
    # total sale
    total_sales = Order.objects.all().aggregate(total_Sales=Sum("order_total"))
    total_sales = total_sales["total_Sales"]
    # todays orders
    today_orders = (
        Order.objects.filter(
            created_at__range=(start_of_day, end_of_day), status="Completed"
        ).aggregate(todays_order_count=Count("order_number"))["todays_order_count"]
        or 0
    )

    # total orders
    total_orders = (
        Order.objects.filter(Q(status="Completed") | Q(status="Cancelled")).aggregate(
            total_orders=Count("order_number")
        )["total_orders"]
        or 0
    )

    context = {
        "orders": orders,
        "order_products": order_products,
        "order_detail": order_detail,
        "today_orders": today_orders,
        "today_sales": today_sales,
        "total_orders": total_orders,
        "total_sales": total_sales,
    }
    return render(request, "admins/sales_report.html", context)


def generate_sales_report_pdf(request):
    orders = Order.objects.filter(Q(status="Completed") | Q(status="Cancelled"))
    order_products = OrderProduct.objects.filter(order__in=orders)
    order_detail = order_details.objects.all()
    order_detail = order_detail.annotate(
        total_discount=F("discount_from_offers") + F("discount_from_coupons")
    )
    # today sale
    current_datetime = timezone.now()
    start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = current_datetime.replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    today_sales = (
        Order.objects.filter(created_at__range=(start_of_day, end_of_day)).aggregate(
            total_sales=Sum("order_total")
        )["total_sales"]
        or 0
    )

    # total sale
    total_sales = Order.objects.all().aggregate(total_Sales=Sum("order_total"))
    total_sales = total_sales["total_Sales"]
    # todays orders
    today_orders = (
        Order.objects.filter(
            created_at__range=(start_of_day, end_of_day), status="Completed"
        ).aggregate(todays_order_count=Count("order_number"))["todays_order_count"]
        or 0
    )

    # total orders
    total_orders = (
        Order.objects.filter(Q(status="Completed") | Q(status="Cancelled")).aggregate(
            total_orders=Count("order_number")
        )["total_orders"]
        or 0
    )

    context = {
        "orders": orders,
        "order_products": order_products,
        "order_detail": order_detail,
        "today_orders": today_orders,
        "today_sales": today_sales,
        "total_orders": total_orders,
        "total_sales": total_sales,
    }

    # Render the HTML template with data
    template = get_template("admins/sales_report_pdf.html")
    html = template.render(context)

    # Enable logging
    pisa.showLogging()

    # Create a PDF response
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    # pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf)

    response = HttpResponse(pdf.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'
    return response


# Create your views here.
