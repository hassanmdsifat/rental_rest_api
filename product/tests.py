from django.test import TestCase

from rest_framework.test import APIRequestFactory

from domain.models.product import Product
from product.views import GetAllProduct


class ProductListTest(TestCase):
    def setUp(self) -> None: 
        all_data_set = [
            {
                "code": "p1",
                "name": "Air Compressor 12 GAS",
                "product_type": "plain",
                "availability": True,
                "needing_repair": False,
                "durability": 3000,
                "max_durability": 3000,
                "mileage": None,
                "price":  4500,
                "minimum_rent_period": 1
            },
            {
                "code": "p2",
                "name": "Air Compressor 5 Electric",
                "product_type": "plain",
                "availability": True,
                "needing_repair": False,
                "durability": 1500,
                "max_durability": 2000,
                "mileage": None,
                "price":  6500,
                "minimum_rent_period": 1
            },
            {
                "code": "p3",
                "name": "Dia Blade 14 inch",
                "product_type": "plain",
                "availability": True,
                "needing_repair": False,
                "durability": 40000,
                "max_durability": 50000,
                "mileage": None,
                "price":  3000,
                "minimum_rent_period": 2
            },
            {
                "code": "p4",
                "name": "Copper Blade 5 inch",
                "product_type": "plain",
                "availability": False,
                "needing_repair": True,
                "durability": 0,
                "max_durability": 2000,
                "mileage": None,
                "price":  200,
                "minimum_rent_period": 2
            },
            {
                "code": "p5",
                "name": "Copper Blade 5 inch",
                "product_type": "plain",
                "availability": False,
                "needing_repair": True,
                "durability": 0,
                "max_durability": 2000,
                "mileage": None,
                "price":  200,
                "minimum_rent_period": 2
            },
            {
                "code": "p6",
                "name": "Copper Blade 8 inch",
                "product_type": "plain",
                "availability": True,
                "needing_repair": False,
                "durability": 1500,
                "max_durability": 2000,
                "mileage": None,
                "price":  300,
                "minimum_rent_period": 2
            },
            {
                "code": "p7",
                "name": "Beam Clamp",
                "product_type": "plain",
                "availability": True,
                "needing_repair": False,
                "durability": 15000,
                "max_durability": 20000,
                "mileage": None,
                "price":  800,
                "minimum_rent_period": 30
            },
            {
                "code": "p8",
                "name": "Beam Clamp",
                "product_type": "plain",
                "availability": True,
                "needing_repair": False,
                "durability": 10000,
                "max_durability": 20000,
                "mileage": None,
                "price":  800,
                "minimum_rent_period": 30
            },
            {
                "code": "p9",
                "name": "Beam Clamp",
                "product_type": "plain",
                "availability": False,
                "needing_repair": False,
                "durability": 5000,
                "max_durability": 20000,
                "mileage": None,
                "price":  800,
                "minimum_rent_period": 30
            },
            {
                "code": "m1",
                "name": "Boom lift 40",
                "product_type": "meter",
                "availability": True,
                "needing_repair": False,
                "durability": 4000,
                "max_durability": 8000,
                "mileage": 10000,
                "price":  1000,
                "minimum_rent_period": 4
            },
            {
                "code": "m2",
                "name": "Boom lift 60",
                "product_type": "meter",
                "availability": True,
                "needing_repair": False,
                "durability": 8000,
                "max_durability": 10000,
                "mileage": 5000,
                "price":  1500,
                "minimum_rent_period": 4
            },
            {
                "code": "m3",
                "name": "Boom lift 80",
                "product_type": "meter",
                "availability": False,
                "needing_repair": True,
                "durability": 500,
                "max_durability": 12000,
                "mileage": 200,
                "price":  2000,
                "minimum_rent_period": 2
            },
            {
                "code": "m4",
                "name": "Boom lift 100",
                "product_type": "meter",
                "availability": True,
                "needing_repair": False,
                "durability": 4000,
                "max_durability": 12000,
                "mileage": 8500,
                "price":  2500,
                "minimum_rent_period": 2
            },
            {
                "code": "m5",
                "name": "Boom lift 20",
                "product_type": "meter",
                "availability": True,
                "needing_repair": False,
                "durability": 1200,
                "max_durability": 8000,
                "mileage": 600,
                "price":  500,
                "minimum_rent_period": 1
            },
            {
                "code": "m6",
                "name": "Boom lift 20",
                "product_type": "meter",
                "availability": True,
                "needing_repair": False,
                "durability": 8000,
                "max_durability": 8000,
                "mileage": 0,
                "price":  500,
                "minimum_rent_period": 1
            },
            {
                "code": "m7",
                "name": "Boom lift 20",
                "product_type": "meter",
                "availability": True,
                "needing_repair": False,
                "durability": 5000,
                "max_durability": 8000,
                "mileage": 1200,
                "price":  500,
                "minimum_rent_period": 1
            },
            {
                "code": "m8",
                "name": "Boom lift 40",
                "product_type": "meter",
                "availability": True,
                "needing_repair": False,
                "durability": 8000,
                "max_durability": 10000,
                "mileage": 2500,
                "price":  1000,
                "minimum_rent_period": 2
            }
        ]
        for data in all_data_set:
            Product.objects.create(**data)
        self.factory = APIRequestFactory()
        self.view = GetAllProduct.as_view()

    def test_product_list(self):
        request = self.factory.get('/api/product/')
        response = self.view(request)
        assert response.status_code == 200
