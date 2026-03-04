from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_id: int | str, timeout: int = 300) -> list:
    """
    Сервисная функция с низкоуровневым кэшированием.
    Возвращает список продуктов в категории с кэшем в Redis.
    """
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

    cache.set(cache_key, products, timeout=timeout)

    return products


def get_all_products(timeout=300) -> list:
    """
    Сервисная функция с низкоуровневым кэшированием.
    Возвращает список всех активных продуктов с кэшем в Redis.
    """
    cache_key = "all_active_products"

    products = cache.get(cache_key)

    if products is not None:
        return products

    products = list(
        Product.objects
        .filter(is_active=True)
        .select_related('category')
        .order_by('name')
    )

    cache.set(cache_key, products, timeout=timeout)

    return products