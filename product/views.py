from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR

from domain.models.product import Product
from product.serializers import ProductSerializer, PriceSerializer, BookingSerializer, BookingDetailsSerializer,\
    ReturnSerializer
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


class BookProduct(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
            'product_id': kwargs['id']
        })
        if serializer.is_valid():
            booking_details = serializer.save()
            booking_details_serializer = BookingDetailsSerializer(booking_details)
            return Response(
                booking_details_serializer.data,
                status=HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=HTTP_400_BAD_REQUEST)


class ReturnProduct(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReturnSerializer

    def get_object(self, product_id):
        return Product.objects.prefetch_related('booking_details').get(id=product_id)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object(kwargs['id'])
            serializer = self.get_serializer(data=request.data, context={
                'product': instance
            })
            if serializer.is_valid():
                booking_details = serializer.save()
                booking_details_serializer = BookingDetailsSerializer(booking_details)
                return Response(
                    booking_details_serializer.data,
                    status=HTTP_200_OK)
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({
                'error': str(E)
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
