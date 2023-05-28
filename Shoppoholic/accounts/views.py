from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, RegisterForm

# Create your views here.
def login_page(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get("next") or request.POST.get("next") or None
    
    context = {
        'title': "Shoppoholic - Login",
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, request.get_host(), True):
                return redirect(next_url)
            return redirect("/")
            # Redirect to success page
        else:...
    return render(request, "accounts/login.html", context)

def logout_page(request):
    logout(request)
    return redirect("/")

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "title": "Shoppoholic - Register",
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        User.objects.create_user(username=username, password=password, email=email)
        return redirect("accounts:login")
    return render(request, "accounts/register.html", context)