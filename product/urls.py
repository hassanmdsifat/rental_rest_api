from django.urls import path
from product.views import GetAllProduct

urlpatterns = [
    path('', GetAllProduct.as_view(), name='all-products'),
]
