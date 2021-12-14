import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from domain.models.product import Product, METER_CHOICE
from domain.models.booking_details import BookingDetails, DONE_STATE, ACTIVE_STATE
from packages.manager.durability_manager import calculate_durability
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


class ReturnSerializer(serializers.Serializer):

    def validate_mileage(self, value):
        product_objects = self.context.get('product')
        if product_objects.product_type == METER_CHOICE and not value:
            raise serializers.ValidationError("Mileage required")
        return value

    actual_rental_date = serializers.DateField(required=True, format=DATE_FORMAT, label='Rental Date')
    actual_return_date = serializers.DateField(required=True, format=DATE_FORMAT, label='Return Date')
    needing_repair = serializers.BooleanField(default=False, label='Need Repairing?')
    mileage = serializers.IntegerField(label='Mileage Used', default=0)

    def validate(self, attrs):
        try:
            current_product = self.context.get('product')
            if current_product.availability:
                raise serializers.ValidationError("Product is not available for return")
            get_price = calculate_price(current_product.id, attrs.get('actual_rental_date'),
                                        attrs.get('actual_return_date'))
            if not get_price['status']:
                raise serializers.ValidationError(get_price['error'])
            attrs['actual_price'] = get_price['price']
            attrs['product_id'] = current_product.id
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object Doesn't exist")
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                current_product = self.context.get('product')
                mileage_used = validated_data.pop('mileage')
                need_repair = validated_data.pop('needing_repair')
                booking_details = current_product.booking_details.filter(booking_state=ACTIVE_STATE).order_by('-id')
                if booking_details:
                    booking_details_object = booking_details.first()
                    booking_details_object.actual_rental_date = validated_data['actual_rental_date']
                    booking_details_object.actual_return_date = validated_data['actual_return_date']
                    booking_details_object.actual_price = validated_data['actual_price']
                    booking_details_object.booking_state = DONE_STATE
                    booking_details_object.save()
                    booking_details_object.refresh_from_db()
                else:
                    data = {**validated_data, 'rental_date': validated_data['actual_rental_date'],
                            'return_date': validated_data['actual_return_date'],
                            'estimated_price': validated_data['actual_price'],
                            'booking_state': DONE_STATE}
                    booking_details_object = BookingDetails.objects.create(**data)
                durability = calculate_durability(validated_data['actual_rental_date'],
                                                  validated_data['actual_return_date'],
                                                  current_product.product_type,
                                                  mileage=mileage_used)
                current_product.availability = True
                current_product.needing_repair = need_repair
                current_product.mileage = current_product.mileage + mileage_used \
                    if current_product.mileage else mileage_used
                current_product.durability -= durability
                current_product.save()
                return booking_details_object
        except Exception as E:
            raise Exception(E)


class BookingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDetails
        fields = '__all__'

