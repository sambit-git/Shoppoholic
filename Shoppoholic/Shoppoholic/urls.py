"""
URL configuration for Shoppoholic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home_page, contact_page, about_page, login_page, register_page, logout_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_page, name="home"),
    path("about", about_page, name="about"),
    path("contact", contact_page, name="contact"),
    path("login", login_page, name="login"),
    path("logout", logout_page, name="logout"),
    path("register", register_page, name="register"),
    path("products/", include("products.urls")),
    path("search/", include("search.urls")),
    path("cart/", include("cart.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)