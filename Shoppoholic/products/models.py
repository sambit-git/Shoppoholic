import os

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models import Q
from .utils import slug_generator

def upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    upload_to = f"products/{instance.title}{ext}"
    while os.path.exists(settings.MEDIA_ROOT / upload_to):
        counter += 1
        upload_to = f"products/{instance.title}{counter}{ext}"
    return upload_to

# Custom QuerySet
class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)
    
    def active(self):
        return self.filter(active=True)
    
    def search(self, query):
        lookups = (
                Q(title__icontains = query) |
                Q(description__icontains = query) |
                Q(tag__title__icontains=query)
            )
        return self.active().filter(lookups).distinct()

# Model Manager
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(model=self.model, using=self.db)
    
    def all(self):
        return self.get_queryset().active()
    def get_by_id(self, id):
        return self.get_queryset().get(id=id)
    
    def featured(self):
        return self.get_queryset().featured()
    
    def search(self, query):
        return self.get_queryset().search(query)

class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=189)
    image       = models.ImageField(upload_to=upload_path, height_field=None, width_field=None, null=True, blank=True)
    active      = models.BooleanField(default=True)
    featured    = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now=True)
    
    objects     = ProductManager()
    
    def __repr__(self) -> str:
        return self.title
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
    
    

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)