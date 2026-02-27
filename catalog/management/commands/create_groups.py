from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа уже существует'))

        # Кастомное право
        unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product',
            content_type__app_label='catalog'
        )
        group.permissions.add(unpublish_perm)

        # Стандартное право на удаление
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type__app_label='catalog'
        )
        group.permissions.add(delete_perm)

        self.stdout.write(self.style.SUCCESS('Все права успешно назначены группе'))