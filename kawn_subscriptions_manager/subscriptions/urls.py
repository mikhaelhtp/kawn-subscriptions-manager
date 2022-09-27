from django.urls import path
from . import views

from kawn_subscriptions_manager.subscriptions.views import (
    list_subscription_plan,
    add_subscription_plan,
    update_subscription_plan,
    delete_subscription_plan,
    subscriptionplan_activate,
    subscriptionplan_deactivate,
    list_client_subscription,
    add_client_subscription,
    deactivate_client_subscription,
    activate_client_subscription,
)

app_name = "subscriptions"
urlpatterns = [
  path("listSubscriptionPlan/", view=list_subscription_plan, name="listSubscriptionPlan"),
  path("addSubscriptionPlan/", view=add_subscription_plan, name="addSubscriptionPlan"),
  path("updateSubscriptionPlan/<int:pk>", view=update_subscription_plan, name="updateSubscriptionPlan"),
  path('deleteSubscriptionPlan/<int:pk>', view=delete_subscription_plan, name='deleteSubscriptionPlan'),
  path('activateSubscriptionPlan/<int:id>', view=subscriptionplan_activate, name='activateSubscriptionPlan'),
  path('deactivateSubscriptionPlan/<int:id>', view=subscriptionplan_deactivate, name='deactivateSubscriptionPlan'),
  path("listClientSubscription/", view=list_client_subscription, name="listClientSubscription"),
  path("addClientSubscription/", view=add_client_subscription, name="addClientSubscription"),
  path('activateClientSubscription/<int:id>', view=activate_client_subscription, name='activateClientSubscription'),
  path('deactivateClientSubscription/<int:id>', view=deactivate_client_subscription, name='deactivateClientSubscription'),
]