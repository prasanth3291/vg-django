from django.contrib import admin
from.models import Product,softdelete,NonDeleted,Variation,Color,Size,Offer,Discount,com_offers

# Define a custom admin action to apply an offer to Men's Shirts
def apply_offer_men_shirts(modeladmin, request, queryset):
    print("Applying offer to Men's Shirts...")  # Debugging print statement
    
    # Filter products in the 'Men' category and 'Shirts' subcategory
    men_shirts = queryset.filter(category__category_name='Men', subcategory__sub_cat_name='Shirts')
    
    try:
        # Retrieve the offer with the name 'men_shirt'
        discount_offer = Offer.objects.get(name='men_shirt')
    except Offer.DoesNotExist:
        discount_offer = None
    
    if discount_offer:
        # Apply the offer to selected products
        men_shirts.update(offer=discount_offer)
        offer_products=Product.objects.filter(offer=discount_offer)
        for product in offer_products:
            variations=Variation.objects.filter(product=product)
            for variation in variations:
                offer_price=variation.price-((variation.price*discount_offer.discount.discount)/100)
                variation.offer_price=offer_price
                variation.save()
        print("Offer applied to Men's Shirts.")
    else:
        print("Offer 'men_shirt' not found.")
def jackets_women(modeladmin, request, queryset):
    women_jackets=queryset.filter(category__category_name='Women', subcategory__sub_cat_name='Jackets')
    try:
        discount_offer=Offer.objects.get(name='women_jackets')
    except Offer.DoesNotExist:
        discount_offer=None
    if discount_offer:
        women_jackets.update(offer=discount_offer)    
        offer_products=Product.objects.filter(offer=discount_offer)
        for product in offer_products:
            variations=Variation.objects.filter(product=product)
            for variation in variations:
                offer_price=variation.price-((variation.price*discount_offer.discount.discount)/100)
                variation.offer_price=offer_price
                variation.save()
        print("Offer applied to Men's Shirts.")
    else:
        print("Offer 'men_shirt' not found.")    
        

# Register the ProductAdmin class with custom actions
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'modified_date', 'is_available', 'offer','category','subcategory')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('is_deleted',)  # Add a filter for soft-deleted products
    actions = ['undelete_selected',apply_offer_men_shirts,jackets_women]  # Define a custom action to undelete products

    def undelete_selected(modeladmin, request, queryset):
        queryset.update(is_deleted=False)  # Set is_deleted to False for selected products
    undelete_selected.short_description = "Undelete selected products"  # Action description
# Register the Product and Offer models with the admin site
admin.site.register(Product, ProductAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display=('product','created_date','is_active','color','size','stock','price','offer_price')#'variation_category','variation_value',
    list_editable=('is_active',)
    list_filter=('product','is_active')#,'variation_value','variation_category'
    
admin.site.register(Variation,VariationAdmin)   
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Discount)
admin.site.register(Offer)
admin.site.register(com_offers)


    

# Register your models here.
