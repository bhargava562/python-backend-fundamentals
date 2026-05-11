from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all() # Similar to productRepository.findAll()
    return render(request, 'catalog/list.html', {'products': products})