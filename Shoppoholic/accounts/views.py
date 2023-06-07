from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri

from .models import GuestEmail
from .forms import LoginForm, RegisterForm, GuestForm

# Create your views here.
def guest_register_page(request):
    form = GuestForm(request.POST or None)
    next_url = request.GET.get("next") or request.POST.get("next") or None
    context = {
        'title': "Shoppoholic - Guest Registration",
        "form": form,
        "formlabel": "Register as a Guest",
        "endpoint": redirect("accounts:register_guest").url
    }
    if form.is_valid():
        email = form.cleaned_data.get("email")
        guest = GuestEmail.objects.create(email=email)
        request.session["guest_id"] = guest.id
        valid_next_url = url_has_allowed_host_and_scheme(
                next_url, request.get_host())
        if valid_next_url:
            return redirect(iri_to_uri(next_url))
        return redirect("/register/")
    else:
            return render(request, "accounts/accounts.html", context)



def login_page(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get("next") or request.POST.get("next") or None
    print(next_url)
    context = {
        'title': "Shoppoholic - Login",
        "form": form,
        "formlabel": "Login to Shoppoholic",
        "endpoint": redirect("accounts:login").url
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            valid_next_url = url_has_allowed_host_and_scheme(
                    next_url, request.get_host())
            print("next url: ", next_url)
            print("isValid: ", valid_next_url)
            if valid_next_url:
                return redirect(iri_to_uri(next_url))
            return redirect("/")
            # Redirect to success page
        else:
            context["err_msg"] = "Email/Password is incorrect"
    return render(request, "accounts/accounts.html", context)

def logout_page(request):
    logout(request)
    return redirect("/")

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "title": "Shoppoholic - Register",
        "form": form,
        "formlabel": "Register with Shoppoholic",
        "endpoint": redirect("accounts:register").url
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        User.objects.create_user(username=username, password=password, email=email)
        return redirect("accounts:login")
    return render(request, "accounts/accounts.html", context)