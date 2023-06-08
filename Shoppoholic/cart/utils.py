from .models import Cart

def update_session_products_count(request):
    cart, _ = Cart.objects.get_or_new(request)
    request.session["products_count"] = len(cart.products.all())