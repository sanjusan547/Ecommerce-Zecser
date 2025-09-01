from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

    
class Productvariant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants')
    name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to='productvariant/',blank=True,null=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"


