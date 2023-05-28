from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL

class CartQuerySet(models.query.QuerySet):
    def get_or_new(self, request):
        cart_id = request.session.get("cart_id", None)
        if request.user.is_authenticated:
            qs = self.filter(Q(id=cart_id) | Q(user=request.user, active=True) )
        else:
            qs = self.filter(id=cart_id)
        if qs.count() == 1:
            is_new = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        elif qs.count() == 2:
            cart1 = qs.first()
            cart2 = qs.last()
            for product in cart1.products.all():
                cart2.products.add(product)
            cart1.delete()
            cart2.save()
            cart_obj = cart2
            is_new = False
        else:
            cart_obj = self.new(user=request.user)
            request.session["cart_id"] = cart_obj.id
            is_new = True
        return cart_obj, is_new
    def new(self, user=None):
        cart_user = None
        if user is not None:
            if user.is_authenticated:
                cart_user = user
        return self.create(user=cart_user)

class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(model=Cart, using=self.db)
    
    def get_or_new(self, request):
        return self.get_queryset().get_or_new(request)
    
    def new(self, user=None):
        return self.get_queryset().create(user=user)

class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE,
                    null= True, blank=True)
    
    products    = models.ManyToManyField(Product, blank=True)
    total       = models.DecimalField(default=0.00, max_digits=25,
                    decimal_places=2)
    
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    
    objects     = CartManager()
    
    def __str__(self) -> str:
        return f"{self.id} - {self.user}"

def m2m_receiver(sender, instance, action, *args, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price
        instance.total = total
        instance.save()
    

m2m_changed.connect(m2m_receiver, sender=Cart.products.through)