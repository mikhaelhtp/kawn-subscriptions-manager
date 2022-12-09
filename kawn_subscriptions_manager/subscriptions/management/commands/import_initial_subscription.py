from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get.get_subscription import get_subscriptions


class Command(BaseCommand):
    help = 'Import API Subscription'

    def handle(self, *args, **kwargs):
        get_subscriptions()