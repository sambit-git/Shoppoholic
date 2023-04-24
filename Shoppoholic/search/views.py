from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product

class SearchView(ListView):
    queryset = Product.objects.all()
    template_name = "search/search_list.html"
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            return qs.search(query)
        return qs.featured()