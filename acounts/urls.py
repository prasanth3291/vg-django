from django.urls import path
from .import views


urlpatterns = [
    path('register',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    # acount activation
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('resest_password_validate/<uidb64>/<token>/',views.resest_password_validate,name='resest_password_validate'),
    path('resest_password',views.reset_password,name='reset_password'),
    
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('manage_adress/',views.manage_adress,name='manage_adress'),
    path('add_adress/',views.add_adress,name='add_adress'),
    path('or_pr_detail/<int:order_product_id>/',views.or_pr_detail,name='or_pr_detail'),
    path('edit_adress/<int:adress_id>/',views.edit_adress,name='edit_adress'),
    path('delete_adress/<int:adress_id>/',views.delete_adress,name='delete_adress'),
    path('coupons/',views.coupons,name='coupons'),
   
    
    
    
    
    
]
