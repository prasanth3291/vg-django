from django import forms
from .models import Acount, UserProfile, Adress, Referal_code, ReviewRating
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForms(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "enter password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Phone Number"})
    )
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Email"}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last name"})
    )
    # add a reference code
    reference_code = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Reference Code"})
    )

    class Meta:
        model = Acount
        fields = ["first_name", "last_name", "email", "password", "phone_number"]

    def clean(self):
        cleaned_data = super(RegistrationForms, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("password does not match")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Acount.objects.filter(email__iexact=email, is_validated=True).exists():
            raise forms.ValidationError("An account with this email  already exists.")
        return email

    def __init__(self, *args, **kwargs):
        super(RegistrationForms, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserForm(forms.ModelForm):
    class Meta:
        model = Acount
        fields = ["first_name", "last_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={"invalid": ("image files only")},
        widget=forms.FileInput,
    )

    class Meta:
        model = UserProfile
        fields = [
            "adress_line1",
            "adress_line2",
            "profile_picture",
            "city",
            "state",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = [
            "name",
            "phone_number",
            "email",
            "adress_line1",
            "adress_line2",
            "pin",
            "city",
            "state",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super(AdressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ["subject", "review", "rating"]
