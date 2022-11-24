from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api import api_outlet


class Command(BaseCommand):
    help = 'Import API Outlet'

    def handle(self, *args, **kwargs):
        api_outlet