from django.core.exceptions import ValidationError
from store.models import Product,Offer,com_offers
from django import forms
from acounts.models import Coupons




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'description',  'is_available', 'category', 'images']# revode- 'price', 'stock',

    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']
        product_id = self.instance.id if self.instance else None  # Get the ID of the current product being edited, if any

        # Check if the product name is unique among existing products
        if Product.objects.exclude(id=product_id).filter(product_name=product_name).exists():
            raise ValidationError("A product with this name already exists.")

        return product_name
    
    
    
class CouponsForm(forms.ModelForm):
    valid_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Use DateField for valid_from    
    valid_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) 
    status = forms.BooleanField(required=False)  # Use BooleanField for status

    class Meta:
        model=Coupons
        fields=['name','discount','valid_from','valid_to','minimum_amount','maximum_discount','coupon_count','status'] 
        
        
    def __init__(self,*args, **kwargs) :
        super(CouponsForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'    


class CategoryOfferForm(forms.ModelForm):
    start_date = forms.DateField(widget = forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(widget = forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model=Offer
        fields=['name','discount','start_date','end_date','description']
    
    def __init__(self,*args,**kwargs):
        super(CategoryOfferForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' 
            
class Minimum_purchaseOfferForm(forms.ModelForm):
    start_date = forms.DateField(widget = forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(widget = forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = com_offers
        fields = ['name','description','discount','start_date','end_date','mimimum_value','maximum_discount'] 
        
    def __init__(self, *args, **kwargs):
        super(Minimum_purchaseOfferForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' 
        
             
            
        