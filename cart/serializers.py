from rest_framework import serializers
from .models import Cart, Cartitem, Wishlist
from product.models import Productvariant,Product
from product.serializers import Variantserializer,Productserializer

class Cartitemserializer(serializers.ModelSerializer):
    product=Variantserializer(read_only=True)
    product_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=Productvariant.objects.all(), source='product', write_only=True
    )
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Cartitem
        fields = ['id', 'product', 'product_variant_id', 'quantity','total_count']

    def get_total_count(self, obj):
        return obj.total_count  

class CartSerializer(serializers.ModelSerializer):
    cartitem = Cartitemserializer(many=True,read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cartitem','total_amount']

    def get_total_amount(self, obj):
        return sum(item.total_count for item in obj.cartitem.all())

class WishlistSerializer(serializers.ModelSerializer):
    products = Productserializer(many=True,read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        write_only=True,
        source='product'
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products', 'product_ids']
        read_only_fields=['user']
