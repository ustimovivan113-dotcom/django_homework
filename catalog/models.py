from django.db import models
from django.contrib.auth.models import User  # Стандартный User

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Активен')  # Исправил is_published на is_active по ДЗ
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # ← обязательно добавить
        blank=True,  # ← обязательно добавить
        verbose_name='Владелец'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')  # Добавил связь с Category

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]