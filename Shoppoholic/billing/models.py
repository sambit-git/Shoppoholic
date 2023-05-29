from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

class BillingProfile(models.Model):
    user        = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    
    email       = models.EmailField(max_length=254)
    active      = models.BooleanField(default=True)
    updated     =models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.email

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)