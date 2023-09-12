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
    
    
]
