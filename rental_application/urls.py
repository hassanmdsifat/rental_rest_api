from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/product/', include('product.urls')),
    path('admin/', admin.site.urls),
]
