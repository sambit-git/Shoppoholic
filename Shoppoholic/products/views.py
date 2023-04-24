from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import Product
from cart.models import Cart

class ProductListView(ListView):
    queryset = Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_new(self.request)
        context["cart"] = cart
        return context

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
