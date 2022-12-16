from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get.get_client import get_clients


class Command(BaseCommand):
    help = 'Import API Clients'

    def handle(self, *args, **kwargs):
        get_clients()