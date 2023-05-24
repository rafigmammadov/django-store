from django.shortcuts import render
from .models import ProductCategory, Product


def index(request):
    context = {
        'title': 'Rafistore',
        'is_promote': True,
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Rafistore-Catalog',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)
