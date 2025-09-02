from django.shortcuts import render

# Create your views here.
# shop/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, Cartitem, Wishlist
from product.models import Product,Productvariant
from .serializers import CartSerializer, Cartitemserializer, WishlistSerializer

# CART
class CartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = request.user.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Cartitemserializer

    def post(self, request):
        cart = request.user.cart
        variant_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        variant = Productvariant.objects.get(id=variant_id)

        item, created = Cartitem.objects.get_or_create(cart=cart, product=variant)
        if not created:
            item.quantity += int(quantity)
            item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart = request.user.cart
        item = cart.cartitem.get(id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# WISHLIST
class WishlistView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = request.user.wishlist
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

class AddToWishlistView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def post(self, request):
        wishlist = request.user.wishlist
        product_ids = request.data.get('product_ids', [])
        variant = Product.objects.get(id=product_ids)
        wishlist.products.add(variant)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

class RemoveFromWishlistView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def delete(self, request,list_id):
        wishlist = request.user.wishlist
        product_id=wishlist.products.get(id=list_id)
        product_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

