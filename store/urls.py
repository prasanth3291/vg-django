

from django.urls import path,include

from.import views

urlpatterns = [
   
    path('', views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:Product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('get_variation_price/', views.get_variation_price, name='get_variation_price'),
    path('Sub_product/<int:category_id>/<int:subcategory_id>/', views.Sub_product, name='Sub_product'),

    
    
    
]

