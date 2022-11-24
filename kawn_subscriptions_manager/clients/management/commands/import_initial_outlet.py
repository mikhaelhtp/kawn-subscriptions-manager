from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get import get_outlet


class Command(BaseCommand):
    help = 'Import API Outlet'

    def handle(self, *args, **kwargs):
        get_outlet