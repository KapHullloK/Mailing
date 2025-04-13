from django.core.management.base import BaseCommand
from django.utils import timezone

from client.models import Mail
from client.services import send_emails


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_emails()
        self.stdout.write(self.style.SUCCESS("Рассылка завершена"))
