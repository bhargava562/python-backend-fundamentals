from django.contrib import admin
from django.urls import path, include
from catalog.views import product_list

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('products/', product_list, name='product-list'),
    path('api/v1/', include('blog.urls')),
]