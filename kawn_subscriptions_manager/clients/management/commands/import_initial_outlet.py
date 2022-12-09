from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get.get_outlet import get_outlets


class Command(BaseCommand):
    help = 'Import API Outlet'

    def handle(self, *args, **kwargs):
        get_outlets()