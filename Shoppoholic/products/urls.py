from django.urls import path

from .views import ProductListView, ProductDetailView, ProductDetailSlugView

app_name = 'products'

urlpatterns = [
    path("", ProductListView.as_view(), name="all"),
    path("<slug>", ProductDetailSlugView.as_view(), name="detail")
]
