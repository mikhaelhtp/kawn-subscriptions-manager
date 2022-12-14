from config import celery_app
from celery import shared_task
from celery import Celery
from celery.schedules import crontab

from kawn_subscriptions_manager.api.api_get.get_subscription_plan import get_subscription_plans
from kawn_subscriptions_manager.api.api_get.get_subscription import get_subscriptions
from kawn_subscriptions_manager.api.api_post.post_subscription_plan import post_subscription_plans
from kawn_subscriptions_manager.api.api_put.put_subscription_plan import put_subscription_plans
from kawn_subscriptions_manager.api.api_put.put_subscription import put_subscriptions

app = Celery()

@shared_task(bind=True)
def get_subscription_plan(self, *args, **kwargs):
    get_subscription_plans()

@shared_task(bind=True)
def get_subscription(self, *args, **kwargs):
    get_subscriptions()

@shared_task(bind=True)
def post_subscription_plan(self, *args, **kwargs):
    post_subscription_plans()

@shared_task(bind=True)
def put_subscription_plan(self, *args, **kwargs):
    put_subscription_plans()

@shared_task(bind=True)
def put_subscription(self, *args, **kwargs):
    put_subscriptions()