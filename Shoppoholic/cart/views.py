from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm

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

def checkout(request):
    cart_obj, _ = Cart.objects.get_or_new(request)
    order_obj, _ = Order.objects.get_or_create(cart=cart_obj)
    print(cart_obj.total)
    if cart_obj.total == 0:
        return redirect("products:all")
    context = {
        "object": order_obj,
        "form": LoginForm(),
        "endpoint": redirect("accounts:login").url,
        "formlabel": "Login to continue checkout"
        }
    return render(request, "cart/checkout.html", context)