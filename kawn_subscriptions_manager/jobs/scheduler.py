from apscheduler.schedulers.background import BackgroundScheduler

from kawn_subscriptions_manager.api.api_get.get_province import get_provinces 
from kawn_subscriptions_manager.api.api_get.get_city import get_cities
from kawn_subscriptions_manager.api.api_get.get_outlet import get_outlets
from kawn_subscriptions_manager.api.api_get.get_subscription_plan import get_subscription_plans
from kawn_subscriptions_manager.api.api_get.get_subscription import get_subscriptions

from kawn_subscriptions_manager.api.api_post.post_outlet import post_outlets
from kawn_subscriptions_manager.api.api_post.post_subscription_plan import post_subscription_plans

from kawn_subscriptions_manager.api.api_put.put_subscription_plan import put_subscription_plans
from kawn_subscriptions_manager.api.api_put.put_subscription import put_subscriptions


def start():
  scheduler = BackgroundScheduler()

  # GET
  scheduler.add_job(get_provinces, 'cron', day_of_week='mon-sun', hour=6, minute=0)
  scheduler.add_job(get_cities, 'cron', day_of_week='mon-sun', hour=6, minute=2)
  scheduler.add_job(get_outlets, 'cron', day_of_week='mon-sun', hour=6, minute=0)
  scheduler.add_job(get_subscription_plans, 'cron', day_of_week='mon-sun', hour=6, minute=0)
  scheduler.add_job(get_subscriptions, 'cron', day_of_week='mon-sun', hour=6, minute=2)

  # POST
  scheduler.add_job(post_subscription_plans, 'cron', day_of_week='mon-fri', hour=18, minute=0)
  scheduler.add_job(post_outlets, 'cron', day_of_week='mon-fri', hour=18, minute=1)

  # PUT
  scheduler.add_job(put_subscription_plans, 'cron', day_of_week='mon-sun', hour=18, minute=0)
  scheduler.add_job(put_subscriptions, 'cron', day_of_week='mon-sun', hour=18, minute=1)

  scheduler.start()