from django import forms


class ProductFilterForm(forms.Form):
    CATEGORY_CHOICES = (
        ("men", "Men"),
        ("women", "Women"),
        ("kids", "Kids"),
    )

    SIZE_CHOICES = (
        ("sm", "SM"),
        ("md", "MD"),
        ("lg", "LG"),
        ("xl", "XL"),
    )

    category = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    size = forms.MultipleChoiceField(
        choices=SIZE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    min_price = forms.DecimalField(
        min_value=0,
        max_value=200,
        required=False,
    )

    max_price = forms.DecimalField(
        min_value=0,
        max_value=200,
        required=False,
    )
