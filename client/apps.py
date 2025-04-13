from time import sleep

from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'

    def ready(self):
        from client.services import start_scheduler
        sleep(2)
        start_scheduler()
