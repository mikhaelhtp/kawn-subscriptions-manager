import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("kawn_subscriptions_manager")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.conf.enable_utc = True
app.conf.timezone = 'Asia/Jakarta'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
# Executes every day morning at 6:00 a.m.
'get_province': {
    'task': 'kawn_subscriptions_manager.clients.tasks.get_province',
    'schedule': crontab(hour=6, minute=0),
}, 
'get_city': {
    'task': 'kawn_subscriptions_manager.clients.tasks.get_city',
    'schedule': crontab(hour=6, minute=1),
},
'get_outlet': {
    'task': 'kawn_subscriptions_manager.clients.tasks.get_outlet',
    'schedule': crontab(hour=6, minute=0),
},
'get_subscription_plan': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.get_subscription_plan',
    'schedule': crontab(hour=6, minute=0),
},
'get_subscription': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.get_subscription',
    'schedule': crontab(hour=6, minute=1),
},
# Executes every day afternoon at 6:00 p.m.
'post_outlet': {
    'task': 'kawn_subscriptions_manager.clients.tasks.post_outlet',
    'schedule': crontab(hour=18, minute=0),
},
'post_subscription_plan': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.post_subscription_plan',
    'schedule': crontab(hour=18, minute=0),
},
# Executes every day afternoon at 6:30 p.m.
'put_subscription_plan': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.put_subscription_plan',
    'schedule': crontab(hour=18, minute=30),
},
'put_subscription': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.put_subscription',
    'schedule': crontab(hour=18, minute=30),
},
}