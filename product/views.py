from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from domain.models.product import Product
from product.serializers import ProductSerializer, PriceSerializer
from packages.manager.price_manager import calculate_price


class GetAllProduct(ListAPIView):
    queryset = Product.objects.all().order_by('id')
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'max_durability', 'mileage', 'price']
    filterset_fields = ['product_type', 'availability', 'needing_repair']
    ordering_fields = ['id', 'code', 'name', 'availability', 'needing_repair', 'mileage']


class GetProductPrice(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PriceSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'from_date': request.query_params.get('from_date', None),
                                               'to_date': request.query_params.get('to_date', None)})
        if serializer.is_valid():
            response_dict = calculate_price(kwargs['id'], serializer.data.get('from_date'),
                                            serializer.data.get('to_date'))
            return Response(response_dict, status=HTTP_200_OK if response_dict['status'] else HTTP_400_BAD_REQUEST)
        return Response(
            {
                'error': serializer.errors
            }
        )
