from django.contrib import admin
from .models import Cart,Cartitem,Wishlist

# Register your models here.
admin.site.register(Cart)
admin.site.register(Wishlist)

@admin.register(Cartitem)
class CartitemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

    def save_model(self, request, obj, form, change):
        if obj.quantity > obj.product.stock:
            from django.core.exceptions import ValidationError
            raise ValidationError(f"Quantity cannot exceed available stock ({obj.product.stock})")
        super().save_model(request, obj, form, change)