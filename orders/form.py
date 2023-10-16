from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "pin",
            "last_name",
            "phone_number",
            "email",
            "adress_line1",
            "adress_line2",
            "country",
            "city",
            "state",
            "order_note",
            "payment",
        ]
