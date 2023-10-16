from django.contrib import admin
from .models import Payment, Order, OrderProduct, order_details


class OrderProductInline(admin.TabularInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "full_name",
        "email",
        "order_total",
        "status",
        "is_ordered",
    ]
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(order_details)


# Register your models here.
