from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Cart, Wishlist

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def createcart_wishlist(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(user=instance)
        Wishlist.objects.create(user=instance)

