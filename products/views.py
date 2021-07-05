from django.shortcuts import render
from .models import Product, ProductCategory


# Create your views here.


def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {'title': 'GeekShop - Каталог'}

    products_list = Product.objects.all()

    context['products'] = products_list
    return render(request, 'products/products.html', context)
