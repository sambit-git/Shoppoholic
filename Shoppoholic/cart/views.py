from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Cart
from products.models import Product

class CartListView(ListView):
    template_name = "cart/home.html"
    def get_queryset(self):
        cart, _ = Cart.objects.get_or_new(self.request)
        return cart

def cart_home(request):
    cart, _ = Cart.objects.get_or_new(request)
    context = {
        "object_list": cart
    }
    return render(request, "cart/home.html", context)

def cart_update(request):
    product = Product.objects.get(id = request.POST.get("product"))
    cart, _ = Cart.objects.get_or_new(request)
    if product in cart.products.all():
        cart.products.remove(product)
    else:
        cart.products.add(product)
    return redirect("products:all")