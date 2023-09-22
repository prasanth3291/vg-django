from django.contrib import admin
from .models import category,Sub_category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','slug')
admin.site.register(category,CategoryAdmin)

class Sub_categoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('sub_cat_name',)}
    list_display=('sub_cat_name','slug')
    

admin.site.register(Sub_category,Sub_categoryAdmin)



# Register your models here.
