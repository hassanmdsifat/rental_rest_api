from django.db import models
from domain.models.base_model import BaseModel

PLAIN_CHOICE = 'plain'
METER_CHOICE = 'meter'

PRODUCT_CHOICES = [
    (PLAIN_CHOICE, 'plain'),
    (METER_CHOICE, 'meter')
]


class Product(BaseModel):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=500)
    product_type = models.CharField(max_length=20, choices=PRODUCT_CHOICES, default=PLAIN_CHOICE)
    availability = models.BooleanField(default=True)
    needing_repair = models.BooleanField(default=False)
    durability = models.IntegerField(default=0)
    max_durability = models.IntegerField(default=0)
    mileage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    minimum_rent_period = models.IntegerField(default=0)

    def __str__(self):
        return "{}-{}".format(self.code, self.name)

    class Meta:
        db_table = 'product'



