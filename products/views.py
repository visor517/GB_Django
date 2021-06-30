from django.shortcuts import render
import os
import json

MODULE_DIR = os.path.dirname(__file__)

# Create your views here.

def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = { 'title': 'GeekShop - Каталог' }
    file_path = os.path.join(MODULE_DIR, 'fixtures/products.json')
    context['products'] = json.load(open(file_path, encoding='utf-8'))
    return render(request, 'products/products.html', context)
