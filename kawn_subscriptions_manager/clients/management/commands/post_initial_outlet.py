from django.core.management.base import BaseCommand
from kawn_subscriptions_manager.api.api_post.post_outlet import post_outlets


class Command(BaseCommand):
    help = 'Post Outlet'

    def handle(self, *args, **kwargs):
        post_outlets()