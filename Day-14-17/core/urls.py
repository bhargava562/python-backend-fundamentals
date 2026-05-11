from django.contrib import admin
from django.urls import path
from catalog.views import product_list

urlpatterns = [
    path('admin/', admin.site.urls),  # <-- Changed .path to .urls
    path('products/', product_list, name='product-list'),
]