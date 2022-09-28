from django.urls import path
from . import views

from kawn_subscriptions_manager.subscriptions.views import (
    list_subscription_plan,
    add_subscription_plan,
    update_subscription_plan,
    delete_subscription_plan,
    activate_subscription_plan,
    deactivate_subscription_plan,
    list_client_subscription,
    add_client_subscription,
    activate_client_subscription,
    deactivate_client_subscription,
)

app_name = "subscriptions"
urlpatterns = [
  path("list/subscription_plan/", view=list_subscription_plan, name="list_subscription_plan"),
  path("add/subscription_plan/", view=add_subscription_plan, name="add_subscription_plan"),
  path("update/subscription_plan/<int:pk>", view=update_subscription_plan, name="update_subscription_plan"),
  path('delete/subscription_plan/<int:pk>', view=delete_subscription_plan, name='delete_subscription_plan'),
  path('activate/subscription_plan/<int:id>', view=activate_subscription_plan, name='activate_subscription_plan'),
  path('deactivate/subscription_plan/<int:id>', view=deactivate_subscription_plan, name='deactivate_subscription_plan'),
  path("list/client_subscription/", view=list_client_subscription, name="list_client_subscription"),
  path("add/client_subscription/", view=add_client_subscription, name="add_client_subscription"),
  path('activate/client_subscription/<int:id>', view=activate_client_subscription, name='activate_client_subscription'),
  path('deactivate/client_subscription/<int:id>', view=deactivate_client_subscription, name='deactivate_client_subscription'),
]