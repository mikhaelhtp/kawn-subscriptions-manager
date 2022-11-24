from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api import api_subscription_plan


class Command(BaseCommand):
    help = 'Import API Subscription Plan'

    def handle(self, *args, **kwargs):
        api_subscription_plan