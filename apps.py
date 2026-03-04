from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'  # Имя приложения
    verbose_name = 'Пользователи'  # Человеческое имя в админке