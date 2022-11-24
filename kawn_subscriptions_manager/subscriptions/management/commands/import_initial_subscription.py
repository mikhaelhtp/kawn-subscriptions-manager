from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get import get_subscription


class Command(BaseCommand):
    help = 'Import API Subscription'

    def handle(self, *args, **kwargs):
        get_subscription