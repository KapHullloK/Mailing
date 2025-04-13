from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from client.models import Mail
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name='Managers')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа Managers создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа Managers уже существует'))

        content_type_mail = ContentType.objects.get_for_model(Mail)
        view_mail_permission = Permission.objects.get(codename='view_mail', content_type=content_type_mail)
        change_mail_permission = Permission.objects.get(codename='change_mail', content_type=content_type_mail)

        content_type_mail_user = ContentType.objects.get_for_model(User)
        view_user_permission = Permission.objects.get(codename='view_user', content_type=content_type_mail_user)
        change_user_permission = Permission.objects.get(codename='change_user', content_type=content_type_mail_user)
        manager_group.permissions.set([
            view_mail_permission,
            view_user_permission,
            change_user_permission,
            change_mail_permission,
        ])
