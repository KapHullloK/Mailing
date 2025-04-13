from django.core.cache import cache

from Mailing.settings import CACHE_ENABLED
from client.models import Mail, Client


def get_mails_from_cache():
    if CACHE_ENABLED:
        key = 'mails'
        cache_data = cache.get(key)
        if cache_data:
            return cache_data

        cache_data = Mail.objects.all()
        cache.set(key, cache_data)
        return cache_data

    return Mail.objects.all()


def get_clients_from_cache():
    if CACHE_ENABLED:
        key = 'clients'
        cache_data = cache.get(key)
        if cache_data:
            return cache_data

        cache_data = Client.objects.all()
        cache.set(key, cache_data)
        return cache_data

    return Client.objects.all()
