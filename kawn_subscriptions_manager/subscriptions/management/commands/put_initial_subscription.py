from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_put.put_subscription import put_subscriptions


class Command(BaseCommand):
    help = 'Put Subscription Plan'

    def handle(self, *args, **kwargs):
        put_subscriptions()