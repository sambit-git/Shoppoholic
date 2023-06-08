from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Cart
from .utils import update_session_products_count
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile
from accounts.models import GuestEmail
from accounts.forms import LoginForm, GuestForm

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
    update_session_products_count(request)
    return redirect("products:all")

def checkout(request):
    cart_obj, _ = Cart.objects.get_or_new(request)
    # order_obj, _ = Order.objects.get_or_create(cart=cart_obj)
    print(cart_obj.total)
    if cart_obj.total == 0:
        return redirect("products:all")
    
    guest_id = request.session.get("guest_id")
    if request.user.is_authenticated:
        billing_obj, _ = BillingProfile.objects.get_or_create(
            user=request.user, email=request.user.email)
    elif guest_id is not None:
        guest_email = GuestEmail.objects.get(id=guest_id)
        billing_obj, _ = BillingProfile.objects.get_or_create(
            email = guest_email)
    else:
        billing_obj = None
    
    if billing_obj is not None:
        order_obj, _ = Order.objects.new_or_get(billing_obj, cart_obj)
    else:
        order_obj = None
    
    context = {
        "object": order_obj,
        "billing_profile": billing_obj,
        "form": LoginForm(),
        "login_endpoint": redirect("accounts:login").url,
        "login_formlabel": "Login to continue checkout",
        "guest_form": GuestForm(request.POST or None),
        "guest_formlabel": "Continue as Guest",
        "guest_endpoint": redirect("accounts:register_guest").url
        }
    
    return render(request, "cart/checkout.html", context)