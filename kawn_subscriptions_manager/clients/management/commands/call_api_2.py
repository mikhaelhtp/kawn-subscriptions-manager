from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api import (
    api_2,
)


class Command(BaseCommand):
    help = 'Call API City and Subscription'

    def handle(self, *args, **kwargs):
        api_2