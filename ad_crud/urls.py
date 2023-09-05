from django.urls import path
from .import views


urlpatterns = [
    path('ad_dashboard',views.ad_dashboard,name='ad_dashboard'),
    path('customers',views.customers,name='customers'),
    path('block_unblock_user/<int:user_id>/',views.block_unblock_user,name='block_unblock_user'),
    path('delete_customer/<int:user_id>/',views.delete_customer,name='delete_customer'),
    path('ad_products',views.ad_products,name='ad_products'),
    path('add_products',views.add_products,name='add_products'),
    path('edit_products/<int:product_id>/',views.edit_products,name='edit_products'),
    path('delete_products/<int:product_id>/',views.delete_products,name='delete_products'),
    path('ad_category',views.ad_category,name='ad_category'),
    path('add_category',views.add_category,name='add_category'),
    path('edit_category/<int:cat_id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:cat_id>/',views.delete_category,name="delete_category")
    
        
]