from django.db import models
from django.db.models.signals import pre_save

from products.models import Product
from products.utils import slug_generator

class Tag(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField(Product, blank=True)
    
    def __str__(self) -> str:
        return self.title

def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)