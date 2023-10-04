

from django.urls import path,include

from.import views

urlpatterns = [
   
    path('', views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:Product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('get_variation_price/', views.get_variation_price, name='get_variation_price'),
    path('Sub_product/<int:category_id>/<int:subcategory_id>/', views.Sub_product, name='Sub_product'),
    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review'),
    path('filter_products',views.filter_products,name='filter_products')
    

    
    
    
]

