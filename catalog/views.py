from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm  # если формы нет — создайте ниже


# ==================== СПИСОК И ДЕТАЛИ ====================
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'


# ==================== СОЗДАНИЕ ====================
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # ← автоматически ставим владельца
        return super().form_valid(form)


# ==================== РЕДАКТИРОВАНИЕ (только владелец) ====================
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("Вы не являетесь владельцем этого продукта.")
        return super().dispatch(request, *args, **kwargs)


# ==================== УДАЛЕНИЕ (владелец ИЛИ модератор) ====================
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_owner = obj.owner == request.user
        is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

        if not (is_owner or is_moderator):
            return HttpResponseForbidden("У вас нет прав на удаление этого продукта.")
        return super().dispatch(request, *args, **kwargs)


# ==================== ОТМЕНА ПУБЛИКАЦИИ (только с правом) ====================
class UnpublishProductView(LoginRequiredMixin, DetailView):
    model = Product

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden("У вас нет прав на отмену публикации.")

        product.is_active = False
        product.save()
        return redirect('product_list')