from .models import CartItem, Carts
from .views import cart_id

# Create a file named wish_list_context_processor.py in one of your Django apps (e.g., myapp/context_processors/wish_list_context_processor.py)

from acounts.models import Wishlist  # Import your Wish List model


def wish_list_count(request):
    wish_list_count = 0

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Count the number of items in the user's wish list
        wish_list_count = Wishlist.objects.filter(user=request.user).count()
        print(wish_list_count)

    return dict(wish_list_count=wish_list_count)


def counter(request):
    cart_count = 0
    if "admin" in request.path:
        return {}
    else:
        try:
            cart = Carts.objects.filter(cart_id=cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Carts.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
