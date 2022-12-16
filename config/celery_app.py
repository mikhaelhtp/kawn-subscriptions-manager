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
app.conf.enable_utc = False
app.conf.use_tz = True
app.conf.timezone = 'Asia/Jakarta'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
# Executes every day morning at 6:00 a.m or 23:00 UTC.
'get_province': {
    'task': 'kawn_subscriptions_manager.clients.tasks.get_province',
    'schedule': crontab(hour=23, minute=0),
}, 
'get_city': {
    'task': 'kawn_subscriptions_manager.clients.tasks.get_city',
    'schedule': crontab(hour=23, minute=1),
},
'get_client': {
    'task': 'kawn_subscriptions_manager.clients.tasks.get_client',
    'schedule': crontab(hour=23, minute=0),
}, 
'get_outlet': {
    'task': 'kawn_subscriptions_manager.clients.tasks.get_outlet',
    'schedule': crontab(hour=23, minute=1),
},
'get_subscription_plan': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.get_subscription_plan',
    'schedule': crontab(hour=23, minute=0),
},
'get_subscription': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.get_subscription',
    'schedule': crontab(hour=23, minute=2),
},
# Executes every day afternoon at 6:00 p.m. or 11:00 UTC
'post_outlet': {
    'task': 'kawn_subscriptions_manager.clients.tasks.post_outlet',
    'schedule': crontab(hour=11, minute=0),
},
'post_subscription_plan': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.post_subscription_plan',
    'schedule': crontab(hour=11, minute=0),
},
# Executes every day afternoon at 6:30 p.m. or 11:30 UTC
'put_subscription_plan': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.put_subscription_plan',
    'schedule': crontab(hour=11, minute=30),
},
'put_subscription': {
    'task': 'kawn_subscriptions_manager.subscriptions.tasks.put_subscription',
    'schedule': crontab(hour=11, minute=30),
},
}