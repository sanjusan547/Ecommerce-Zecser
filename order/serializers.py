from rest_framework import serializers
from .models import Address,Order

class Addressserializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'
        read_only_fields=['user']


class Orderserializer(serializers.ModelSerializer):
    address=Addressserializer
    class Meta:
        model=Order
        fields=['address','id','user','is_paid','amount']
        read_only_fields=['user','is_paid','amount']