from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')  # добавь created_at, если есть в модели
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')