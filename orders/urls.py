

from django.urls import path,include
from .views import place_order,payments

from.import views

urlpatterns = [
   
   path('place_order/',views.place_order,name='place_order'),
   path('payments/<str:order_number>/',views.payments,name='payments'),
   path('cancel_order/<str:order_number>/', views.cancel_order, name='cancel_order'),
   path('order_complete',views.order_complete,name='order_complete'),
   path('generate_invoice_pdf/<int:order_id>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
   path('pdf_view/<int:order_id>/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/<int:order_id>/', views.DownloadPDF.as_view(), name="pdf_download"),

   
    
]

