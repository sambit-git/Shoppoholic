from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        guest_id = request.session.get("guest_id")
        if request.user.is_authenticated:
            obj, created = self.model.objects.get_or_create(
                user=request.user, email=request.user.email)
        elif guest_id is not None:
            guest_email = GuestEmail.objects.get(id=guest_id)
            obj, created = self.model.objects.get_or_create(
                email = guest_email)
        else:
            obj, created = None, False
        
        return obj, created

class BillingProfile(models.Model):
    user        = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    
    email       = models.EmailField(max_length=254)
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    objects     = BillingProfileManager()
    
    def __str__(self) -> str:
        return self.email

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)