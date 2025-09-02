from django.contrib import admin
from .models import Cart,Cartitem,Wishlist

# Register your models here.
admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(Wishlist)