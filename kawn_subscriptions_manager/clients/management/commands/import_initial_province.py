from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get import get_province


class Command(BaseCommand):
    help = 'Import API Province'

    def handle(self, *args, **kwargs):
        get_province