from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .services import get_products_by_category
from .models import Category


@cache_page(60 * 10)  # 10 минут — хороший баланс; можно 900 (15 мин)
def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # лучше сразу 404, чем ручной if

    products = get_products_by_category(category_id)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/products_by_category.html', context)