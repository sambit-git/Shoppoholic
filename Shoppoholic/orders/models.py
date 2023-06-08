import random
import string

from django.db import models
from django.db.models.signals import pre_save, post_save

from billing.models import BillingProfile
from cart.models import Cart

ORDER_STATUS_CHOICES = (
('created', 'Created'),
('shipped', 'Shipped'),
('out for delivery', 'Out for delivery'),
('delivered', 'Delivered'),
('return requested', 'Return requested'),
('cancelled', 'Cancelled'),
('refunded', 'Refunded')
)

class Order(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    
    order_id        = models.CharField(max_length=120, blank=True, null=True)
    
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    
    status          = models.CharField(
        max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    
    shipping_total  = models.DecimalField(
        default=40, max_digits=100, decimal_places=2)
    
    total           = models.DecimalField(
        default=40, max_digits=100, decimal_places=2)
    
    active          = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        super().__str__()
        return str(self.order_id)
    
    def update_total(self):
        total = self.cart.total + self.shipping_total
        if self.total != total:
            self.total = total
            self.save()
    
def unique_id_generator(instance, order_id=None):
    cls = instance.__class__
    qs = cls.objects.filter(order_id=order_id)
    if qs.exists() or order_id is None:
        new_order_id = "".join(
            random.choice(
                string.ascii_lowercase+string.digits)
                for _ in range(20))
        return unique_id_generator(instance, new_order_id)
    return order_id

def presave_order_connector(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_id_generator(instance)

pre_save.connect(presave_order_connector, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        qs = Order.objects.filter(cart__id=instance.id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order_total(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order_total, sender=Order)