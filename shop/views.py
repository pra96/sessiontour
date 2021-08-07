from django.http import JsonResponse
from django.shortcuts import render
from shop.utils import *
from . models import *


# JSON API urls for handling user data
def update_item(request):
    process_cart(request)
    return JsonResponse('Item was added', safe=False)


def process_order(request):
    process_user_data(request)
    return JsonResponse('Payment submitted...', safe=False)


# Shop page URLs
def shop(request):
    context = make_context(request)
    context['products'] = Product.objects.all()
    return render(request, 'shop/catalog.html', context)


def cart(request):
    context = make_context(request)
    return render(request, 'shop/cart.html', context)


def checkout(request):
    context = make_context(request)
    return render(request, 'shop/checkout.html', context)
