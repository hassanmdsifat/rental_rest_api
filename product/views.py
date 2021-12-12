from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from domain.models.product import Product
from product.serializers import ProductSerializer


class GetAllProduct(ListAPIView):
    queryset = Product.objects.all().order_by('id')
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'max_durability', 'mileage', 'price']
    filterset_fields = ['product_type', 'availability', 'needing_repair']
    ordering_fields = ['id', 'code', 'name', 'availability', 'needing_repair', 'mileage']
