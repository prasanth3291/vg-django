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
    path('delete_category/<int:cat_id>/',views.delete_category,name="delete_category"),
    path('order_details_admin/<int:order_id>/',views.order_details_admin,name='order_details_admin'),    
    path('orders',views.orders,name='orders'),
    path('coupons',views.coupons,name='coupons'),
    path('add_coupons',views.add_coupons,name='add_coupons'),
    path('edit_coupons/<int:coupon_id>/',views.edit_coupons,name='edit_coupons'),    
    path('delete_coupons/<int:coupon_id>/',views.delete_coupons,name='delete_coupons'),    
    path('profiles/<int:customer_id>/',views.profiles,name='profiles'),
    path('ad_refer',views.ad_refer,name='ad_refer'),
    path('minimum_purchase_offers',views.minimum_purchase_offers,name='minimum_purchase_offers'),
    path('category_offers',views.category_offers,name='category_offers'),
    path('edit_category_offer/<int:offer_id>/',views.edit_category_offer,name='edit_category_offer'),
    path('add_category_offer',views.add_category_offer,name='add_category_offer'),
    path('delete_category_offer/<int:offer_id>/',views.delete_category_offer,name='delete_category_offer'),
    path('edit_minimum_purchaseoffer/<int:offer_id>/',views.edit_minimum_purchase_offer,name='edit_minimum_purchase_offer'),
    path('add_minimum_purchase_offer',views.add_minimum_purchase_offer,name='add_minimum_purchase_offer'),
    path('delete_minimum_purchase_offer/<int:offer_id>/',views.delete_minimum_purchase_offer,name='delete_minimum_purchase_offer'),
    path('sales_report',views.sales_report,name='sales_report'),
    path('generate_sales_report_pdf', views.generate_sales_report_pdf, name='generate_sales_report_pdf'),
     

     


    
        
]
