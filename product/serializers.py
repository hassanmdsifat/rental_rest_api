from rest_framework import serializers
from domain.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PriceSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=True, format="%Y-%m-%d")
    to_date = serializers.DateField(required=True, format="%Y-%m-%d")
