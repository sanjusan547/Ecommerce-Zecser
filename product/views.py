from django.shortcuts import render
from rest_framework import viewsets
from .models import Product,Productvariant,Category
from .serializers import Productserializer,Variantserializer,Categoryserializer
from rest_framework.permissions import IsAdminUser


class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=Productserializer
    permission_classes=[IsAdminUser]

class VariantView(viewsets.ModelViewSet):
    queryset=Productvariant.objects.all()
    serializer_class=Variantserializer
    permission_classes=[IsAdminUser]

class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer
    permission_classes=[IsAdminUser]
