from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_post import post_subscription_plan


class Command(BaseCommand):
    help = 'Post Subscription Plan'

    def handle(self, *args, **kwargs):
        post_subscription_plan