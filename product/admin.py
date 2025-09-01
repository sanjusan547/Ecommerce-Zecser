from django.contrib import admin
from .models import Category,Product,Productvariant

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']


class ProductVariantInline(admin.TabularInline):
    model = Productvariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active','description','image']
    inlines = [ProductVariantInline]

@admin.register(Productvariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name','price', 'stock','image']