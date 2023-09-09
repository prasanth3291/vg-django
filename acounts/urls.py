from django.urls import path
from .import views


urlpatterns = [
    path('register',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    # acount activation
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard')
    
]
