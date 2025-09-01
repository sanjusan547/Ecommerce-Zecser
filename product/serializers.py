from rest_framework import serializers
from .models import Product,Productvariant,Category


class Variantserializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model=Productvariant
        fields = ['id', 'name', 'price', 'stock', 'image','product']
        read_only_fields=['product']  

class Productserializer(serializers.ModelSerializer):
    variants=Variantserializer(many=True,required=False)

    class Meta:
        model=Product
        fields='__all__'
        read_only_fields=['created_at','updated_at']

    def create(self,validated_data):
        variant=validated_data.pop('variants',[])
        product=Product.objects.create(**validated_data)
        for variants in variant:
            Productvariant.objects.create(product=product,**variants)
        return product
    
    def update(self,instance,validated_data):
        variant_datas=validated_data.pop('variants',[])
        for attrs,value in validated_data.items():
            setattr(instance,attrs,value)
        instance.save()
        

        for variant_data in variant_datas:
            variant_id = variant_data.get('id', None)
            if variant_id:
                try:
                    variant_obj=Productvariant.objects.get(id=variant_id, product=instance)
                    print("Updating variant:", variant_id, variant_data)  # DEBUG
                    for attr, value in variant_data.items():
                        if attr != "id": 
                            setattr(variant_obj, attr, value)
                    variant_obj.save()
                except Productvariant.DoesNotExist:
                    continue
            else:
               if not Productvariant.objects.filter(
                   product=instance,
                   name=variant_data.get("name")
                   ).exists():
                   print("Creating new variant:", variant_data)
                   Productvariant.objects.create(product=instance, **variant_data)
           

        return instance
    
class Categoryserializer(serializers.ModelSerializer):
    products=Productserializer(many=True,read_only=True)

    class Meta:
        model=Category
        fields=('name','id','products')
        
