from django.core.exceptions import ValidationError
from store.models import Product
from django import forms


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
