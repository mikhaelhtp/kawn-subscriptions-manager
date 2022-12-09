from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_get.get_subscription_plan import get_subscription_plans


class Command(BaseCommand):
    help = 'Import API Subscription Plan'

    def handle(self, *args, **kwargs):
        get_subscription_plans()