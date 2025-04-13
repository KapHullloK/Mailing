from django.core.management.base import BaseCommand

from blog.models import Blog
from users.models import User
from client.models import Client, Message, Mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email='admin@my.com',
            defaults={
                'password': 'admin',
                'is_superuser': True,
                'is_staff': True,
            }
        )
        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь создан: admin@my.com | admin'))

        clients = []
        for i in range(5):
            client = Client.objects.create(
                email=f'client{i}@example.com',
                full_name=f'Client {i}',
                comment=f'This is client {i}',
                owner=user
            )
            clients.append(client)

        messages = []
        for i in range(3):
            message = Message.objects.create(
                topic=f'Message Topic {i}',
                message=f'This is the content of message {i}',
                owner=user
            )
            messages.append(message)

        for i in range(3):
            mail = Mail.objects.create(
                time_for_sending='2025-04-15T10:00:00Z',
                periodicity='week',
                message=messages[i],
                owner=user
            )

            mail.recipients.set(clients[:i + 1])
            mail.save()

        for i in range(4):
            blog = Blog.objects.create(
                title=f'Blog Title {i}',
                content='hello'
            )
            blog.save()

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми данными'))
