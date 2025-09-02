# shop/urls.py
from django.urls import path
from .views import (
    CartView, AddToCartView, RemoveCartItemView,
    WishlistView, AddToWishlistView, RemoveFromWishlistView
)

urlpatterns = [
    path('cart-view/', CartView.as_view(), name='cart'),
    path('cart-add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart-view/<int:item_id>/', RemoveCartItemView.as_view(), name='remove_cart_item'),

    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist-add/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist-remove/<int:list_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]
