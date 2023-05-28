from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home_page, contact_page, about_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_page, name="home"),
    path("about", about_page, name="about"),
    path("contact", contact_page, name="contact"),
    path("accounts/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("search/", include("search.urls")),
    path("cart/", include("cart.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)