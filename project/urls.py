from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Админ-панель (оставляем)
    path('', include('catalog.urls')),  # Корень ('') теперь включает catalog.urls, так что / откроет ProductListView
]