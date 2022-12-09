from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get.get_city import get_cities


class Command(BaseCommand):
    help = 'Import API City'

    def handle(self, *args, **kwargs):
        get_cities()