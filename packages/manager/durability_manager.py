import logging

from domain.models.product import PLAIN_CHOICE
from packages.helper.converter import convert_str_to_date

logger = logging.getLogger(__name__)


def calculate_durability(from_date, to_date, product_type, mileage=0):
    if type(from_date) == str:
        from_date = convert_str_to_date(from_date)
    if type(to_date) == str:
        to_date = convert_str_to_date(to_date)

    day_spent = (to_date - from_date).days
    if product_type == PLAIN_CHOICE:
        durability = day_spent
    else:
        durability = (day_spent * 2) + ((mileage // 10) * 2)
    return durability

