

from django.urls import path,include

from.import views

urlpatterns = [
   
    path('', views.store,name='store'),
    path('<slug:category_slug>/',views.store,name='product_by_category'),
    path('<slug:category_slug>/<slug:Product_slug>/',views.product_detail,name='product_detail')
    
    
]

