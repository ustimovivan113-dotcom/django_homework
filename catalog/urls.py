from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, UnpublishProductView,
    ProductsByCategoryView  # Добавили импорт
)

app_name = 'catalog'  # Для namespace в urls

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/unpublish/', UnpublishProductView.as_view(), name='product_unpublish'),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),  # Добавили
]