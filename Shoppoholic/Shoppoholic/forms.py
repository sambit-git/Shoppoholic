from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control m-2",
            "placeholder": "Full Name"
        }
    ), label="")
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control m-2",
            "placeholder": "example@domain.com"
        }
    ), label="")
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control m-2",
            "placeholder": "Write your thoughts/concerns here"
        }
    ), label="")
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "@gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    def clean_email(self):
        email = super().clean().get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email already taken.")
        return email
    
    def clean_username(self):
        username = super().clean().get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username already taken.")
        return username
        
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("passwords must match")
        return cleaned_data