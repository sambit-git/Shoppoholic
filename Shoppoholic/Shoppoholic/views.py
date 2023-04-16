from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model

from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    context = {
        'title': "Shoppoholic - Home",
        "content": "Home Page",
        "premium_content": "YEAAAHHHHH"
        }
    return render(request, "homepage.html", context)


def about_page(request):
    context = {
        'title': "Shoppoholic - Home",
        "content": "About Page"
        }
    return render(request, "homepage.html", context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    context = {
        'title': "Shoppoholic - Home",
        "content": "Contact Page",
        "form": form
        }
    if form.is_valid():
        print(form.cleaned_data)
    # if request.method == "POST":
    #     print("Full name", request.POST.get("fullname"))
    #     print("Email", request.POST.get("email"))
    #     print("Message", request.POST.get("content"))
    #     print(request.POST)
        # print(request.cleaned_data)
    return render(request, "contact/view.html", context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'title': "Shoppoholic - Login",
        "form": form
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # context["form"] = LoginForm()
            return redirect("/")
            # Redirect to success page
        else:
            print("Error")
    print(request.user.is_authenticated)
    return render(request, "auth/login.html", context)

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
        return redirect("/login")
    return render(request, "auth/register.html", context)