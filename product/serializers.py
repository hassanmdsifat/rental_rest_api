import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from domain.models.product import Product
from domain.models.booking_details import BookingDetails
from packages.manager.price_manager import calculate_price

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PriceSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=True, format=DATE_FORMAT)
    to_date = serializers.DateField(required=True, format=DATE_FORMAT)


class BookingSerializer(serializers.Serializer):
    rental_date = serializers.DateField(required=True, format=DATE_FORMAT)
    return_date = serializers.DateField(required=True, format=DATE_FORMAT)

    def validate(self, attrs):
        current_product_id = self.context.get('product_id', None)
        try:
            current_product = Product.objects.get(id=current_product_id)
            if not current_product.availability:
                raise serializers.ValidationError("Product is not available for booking")
            get_price = calculate_price(current_product_id, attrs.get('rental_date'), attrs.get('return_date'))
            if not get_price['status']:
                raise serializers.ValidationError(get_price['error'])
            attrs['estimated_price'] = get_price['price']
            attrs['product_id'] = current_product_id
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object Doesn't exist")
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                booking_object = BookingDetails.objects.create(**validated_data)
                Product.objects.filter(id=validated_data.get('product_id')).update(availability=False)
                return booking_object
        except Exception as E:
            logger.error(str(E))
        return None


class BookingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDetails
        fields = '__all__'

