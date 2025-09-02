from django.db import models
from django.conf import settings
from product.models import Product,Productvariant

class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart of {self.user}"

class Cartitem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitem')
    product=models.ForeignKey(Productvariant,on_delete=models.CASCADE,related_name='cartproduct')
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_count(self):
        return self.product.price * self.quantity
    
class Wishlist(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='wishlist')
    products=models.ManyToManyField(Product,blank=True,related_name='wishlists')

    def __str__(self):
        return f"{self.user} wishlist"