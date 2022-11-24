from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api import api_province


class Command(BaseCommand):
    help = 'Import API Province'

    def handle(self, *args, **kwargs):
        api_province