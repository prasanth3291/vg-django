from django.contrib import admin
from.models import Product,softdelete,NonDeleted,Variation,Color,Size


class ProductAdmin(admin.ModelAdmin):
    list_display        =('product_name','modified_date','is_available') #,'price','stock'
    prepopulated_fields ={'slug':('product_name',)}
    
admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display=('product','created_date','is_active','color','size','stock')#'variation_category','variation_value',
    list_editable=('is_active',)
    list_filter=('product','is_active')#,'variation_value','variation_category'
    
admin.site.register(Variation,VariationAdmin)   
admin.site.register(Color)
admin.site.register(Size)

    

# Register your models here.
