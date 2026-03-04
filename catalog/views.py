from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category, get_all_products  # Добавили get_all_products

# Список всех продуктов (эндпоинт для просмотра всех продуктов)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return get_all_products()  # Используем сервис с низкоуровневым кэшем

# Детальная страница одного продукта (с кэшированием страницы)
@method_decorator(cache_page(60 * 15), name='dispatch')  # 15 минут = 900 секунд
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# Создание продукта
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# Обновление продукта
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

# Удаление продукта
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

# Отключение публикации продукта (unpublish)
class UnpublishProductView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.user.has_perm('catalog.can_unpublish_product') or product.owner == request.user:
            product.is_active = False
            product.save()
        return redirect('catalog:product_list')

# Продукты по категории (с кэшированием страницы)
@method_decorator(cache_page(60 * 10), name='dispatch')  # 10 минут = 600 секунд
class ProductsByCategoryView(View):
    template_name = 'catalog/products_by_category.html'

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = get_products_by_category(category_id)

        context = {
            'category': category,
            'products': products,
            'title': f"Товары в категории: {category.name}",
        }
        return render(request, self.template_name, context)