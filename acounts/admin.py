from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import Acount,UserProfile,Adress,Coupons
from django.utils.html import format_html 
from django.utils import timezone



def aplly_WL30(modeladmin, request, queryset):
    eligible_date=timezone.now()-timezone.timedelta(days=30)
    user_wl=Acount.objects.filter(date_joined__gte=eligible_date)
    
    try:
        coupon=Coupons.objects.get(name='WL-30',status=True)
      
    except coupon.DoesNotExist:
        coupon=None
        
    for user in user_wl:
            user.coupons_set.add(coupon)            
            
def aplly_ING40(modeladmin, request, queryset):
    eligible_date=timezone.now()-timezone.timedelta(days=30)
    user_ING=Acount.objects.filter(date_joined__gte=eligible_date)
    
    try:
        coupon=Coupons.objects.get(name='ING-40',status=True)
      
    except coupon.DoesNotExist:
        coupon=None
        
    for user in user_ING:
            user.coupons_set.add(coupon)              

class AcountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links=('email','first_name','last_name')
    readonly_fields=('last_login','date_joined',)
    ordering=('-date_joined',)
    
    filter_horizontal=()
    list_filter=()
    fieldsets=() 
    
    
    
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style=border-radius:50%;>'.format(object.profile_picture.url))
    thumbnail.short_description='Profile Picture'
        
    list_display=('thumbnail','user','city','state','country')    
    
class CouponsAdmin(admin.ModelAdmin):
    list_display=('name','discount','valid_from','valid_to','status') 
    actions=[aplly_WL30,aplly_ING40]   
    
    

admin.site.register(Acount,AcountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Adress)
admin.site.register(Coupons,CouponsAdmin)

# Register your models here.
