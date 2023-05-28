from django.urls import path

from .views import CartListView, cart_home, cart_update, checkout

app_name = "cart"

urlpatterns = [
    path("", CartListView.as_view(), name="home"),
    # path("", cart_home, name="home"),
    path("update", cart_update, name="update"),
    path("checkout", checkout, name="checkout"),
]