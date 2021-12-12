from rest_framework.serializers import ModelSerializer
from domain.models.product import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
