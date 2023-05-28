from django.shortcuts import render

from .forms import ContactForm

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
    return render(request, "contact/view.html", context)