from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class GuestForm(forms.Form):
    email   = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control mt-2 mb-2",
        "placeholder": "Guest Email ID"
    }), label="")

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control mt-2 mb-2",
        "placeholder": "username"
    }), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control mt-2 mb-2",
        "placeholder": "password"
    }), label='')

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control mt-2 mb-2",
        "placeholder": "username"
    }), label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control mt-2 mb-2",
        "placeholder": "email"
    }), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control mt-2 mb-2",
        "placeholder": "password"
    }), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control mt-2 mb-2",
        "placeholder": "Confirm Password"
    }), label="")
    
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