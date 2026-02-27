# ------------------ Кэширование ------------------

# Обычно в самом конце файла

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',   # /1 — номер базы (можно 0, но лучше отдельная)
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'my_django_project',        # чтобы не пересекаться с другими проектами
    }
}

# Опционально — удобная переменная для включения/выключения кэша (очень полезно на проде/тесте)
CACHE_ENABLED = True   # или os.getenv("CACHE_ENABLED", "True").lower() == "true"

# Если хочешь гибко включать/выключать кэш в разработке
if not CACHE_ENABLED:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }