from config import celery_app
from celery import shared_task
from celery import Celery
from celery.schedules import crontab

from kawn_subscriptions_manager.api.api_get.get_province import get_provinces
from kawn_subscriptions_manager.api.api_get.get_city import get_cities
from kawn_subscriptions_manager.api.api_get.get_client import get_clients
from kawn_subscriptions_manager.api.api_get.get_outlet import get_outlets
from kawn_subscriptions_manager.api.api_post.post_outlet import post_outlets

app = Celery()

@shared_task(bind=True)
def get_province(self, *args, **kwargs):
    get_provinces()

@shared_task(bind=True)
def get_city(self, *args, **kwargs):
    get_cities()

@shared_task(bind=True)
def get_client(self, *args, **kwargs):
    get_clients()

@shared_task(bind=True)
def get_outlet(self, *args, **kwargs):
    get_outlets()

@shared_task(bind=True)
def post_outlet(self, *args, **kwargs):
    post_outlets()