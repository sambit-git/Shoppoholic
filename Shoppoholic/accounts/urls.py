from django.urls import path

from .views import login_page, register_page, logout_page, guest_register_page

app_name = "accounts"

urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/guest/", guest_register_page, name="register_guest"),
    path("logout/", logout_page, name="logout"),
    path("register/", register_page, name="register"),
]
