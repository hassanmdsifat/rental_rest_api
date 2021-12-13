from django.urls import path
from product.views import GetAllProduct, GetProductPrice, BookProduct

urlpatterns = [
    path('', GetAllProduct.as_view(), name='all-products'),
    path('<int:id>/price/', GetProductPrice.as_view(), name='product-price'),
    path('<int:id>/book/', BookProduct.as_view(), name='book-product'),
]
