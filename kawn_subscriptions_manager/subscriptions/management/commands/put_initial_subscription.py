from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_put import put_subscription


class Command(BaseCommand):
    help = 'Put Subscription Plan'

    def handle(self, *args, **kwargs):
        put_subscription