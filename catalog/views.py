from django.shortcuts import render
from .services import get_products_by_category
from .models import Category


def products_by_category(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    if not category:
        # можно 404, но для простоты
        return render(request, 'catalog/products_by_category.html', {'error': 'Категория не найдена'})

    products = get_products_by_category(category_id)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/products_by_category.html', context)