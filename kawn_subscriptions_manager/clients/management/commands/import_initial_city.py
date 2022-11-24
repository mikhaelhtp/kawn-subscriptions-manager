from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api import api_city


class Command(BaseCommand):
    help = 'Import API City'

    def handle(self, *args, **kwargs):
        api_city