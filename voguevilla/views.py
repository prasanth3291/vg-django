from django.shortcuts import render
from store.models import Product
from django.views.decorators.cache import never_cache


@never_cache
def home(request):
    products = (
        Product.objects.all().filter(is_available=True).order_by("-created_date")[:8]
    )

    context = {"products": products}

    return render(request, "home.html", context)


# Create your views here.
