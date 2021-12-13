from django.urls import path
from product.views import GetAllProduct, GetProductPrice, BookProduct, ReturnProduct

urlpatterns = [
    path('', GetAllProduct.as_view(), name='all-products'),
    path('<int:id>/price/', GetProductPrice.as_view(), name='product-price'),
    path('<int:id>/book/', BookProduct.as_view(), name='book-product'),
    path('<int:id>/return/', ReturnProduct.as_view(), name='return-product'),
]
