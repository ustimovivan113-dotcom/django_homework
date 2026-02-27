from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_id: int | str, timeout=300) -> list:
    cache_key = f"products_category_{category_id}"

    products = cache.get(cache_key)

    if products is not None:
        return products

    category = Category.objects.filter(id=category_id).first()
    if not category:
        return []

    products = list(
        Product.objects
        .filter(category=category, is_active=True)
        .select_related('category')
        .order_by('name')
    )

    # Сохраняем в кэш на 5 минут (300 секунд)
    cache.set(cache_key, products, timeout=timeout)

    return products