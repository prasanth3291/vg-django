from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Acount,
    UserProfile,
    Adress,
    Coupons,
    Wishlist,
    Referal_code,
    ReviewRating,
    Wallet,
    Transaction,
)
from django.utils.html import format_html
from django.utils import timezone


class AcountAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "last_login",
        "date_joined",
        "is_active",
    )
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = (
        "last_login",
        "date_joined",
    )
    ordering = ("-date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(
            '<img src="{}" width="30" style=border-radius:50%;>'.format(
                object.profile_picture.url
            )
        )

    thumbnail.short_description = "Profile Picture"

    list_display = ("thumbnail", "user", "city", "state", "country")


class CouponsAdmin(admin.ModelAdmin):
    list_display = ("name", "discount", "valid_from", "valid_to", "status")

    # actions=[aplly_WL30,aplly_ING40]


class Referal_codeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "referrer_user",
        "referred_user",
        "gift_money",
        "is_activated",
    )


admin.site.register(Referal_code, Referal_codeAdmin)
admin.site.register(Acount, AcountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Adress)
admin.site.register(Coupons, CouponsAdmin)
admin.site.register(Wishlist)
admin.site.register(ReviewRating)
admin.site.register(Wallet)
admin.site.register(Transaction)

# Register your models here.
