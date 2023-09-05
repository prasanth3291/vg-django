from django import forms
from .models import Acount

class RegistrationForms(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'enter password'})) 
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm password'}))    
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Phone Number'}))  # new


    
    class Meta:
        model=Acount
        fields=['first_name','last_name','email','password','phone_number']
        
        
    def clean(self):
       cleaned_data=super(RegistrationForms,self).clean()    
       password=cleaned_data.get('password')
       confirm_password=cleaned_data.get('confirm_password')
       
       
       if password != confirm_password:
           raise forms.ValidationError(
               'password does not match'
               
           ) 
        