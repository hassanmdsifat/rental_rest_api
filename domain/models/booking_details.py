from django.db import models
from domain.models import BaseModel, Product

ACTIVE_STATE = 'running'
DONE_STATE = 'complete'

BOOKING_STATE_CHOICES = [
    (ACTIVE_STATE, 'Running'),
    (DONE_STATE, 'complete')
]


class BookingDetails(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='booking_details')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_date = models.DateField()
    return_date = models.DateField()
    actual_rental_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    booking_state = models.CharField(max_length=10, choices=BOOKING_STATE_CHOICES, default=ACTIVE_STATE)
