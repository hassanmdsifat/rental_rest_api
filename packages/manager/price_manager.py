import logging

from domain.models.product import Product
from packages.helper.converter import convert_str_to_date

logger = logging.getLogger(__name__)


def calculate_price(product_id, from_date, to_date):
    return_dict = {
        'status': True,
        'price': 0,
        'error': ''
    }
    try:
        current_product = Product.objects.get(id=product_id)
        if type(from_date) == str:
            from_date = convert_str_to_date(from_date)
        if type(to_date) == str:
            to_date = convert_str_to_date(to_date)
        day_spent = (to_date-from_date).days

        if current_product.discount_price:
            calculated_price = current_product.price * day_spent
            if day_spent > current_product.minimum_rent_period:
                calculated_price -= current_product.discount_price
            return_dict['price'] = calculated_price
        else:
            if day_spent <= current_product.minimum_rent_period:
                return_dict['status'] = False
                return_dict['error'] = 'Rental Period is not minimum rent period'
            else:
                calculated_price = current_product.price * day_spent
                return_dict['price'] = calculated_price
    except Exception as E:
        logger.error(str(E), exc_info=True)
        return_dict['status'] = False
        return_dict['error'] = str(E)
    return return_dict
