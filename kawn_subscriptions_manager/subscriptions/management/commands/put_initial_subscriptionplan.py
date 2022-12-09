from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_put.put_subscription_plan import put_subscription_plans


class Command(BaseCommand):
    help = 'Put Subscription Plan'

    def handle(self, *args, **kwargs):
        put_subscription_plans()