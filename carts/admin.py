from django.contrib import admin
from .models import CartItem,Carts,UserCoupons



class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','date_added')
    
    

class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')    
    

admin.site.register(Carts,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(UserCoupons)



# Register your models here.
