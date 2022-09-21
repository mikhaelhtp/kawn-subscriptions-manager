from django.urls import path
from kawn_subscriptions_manager.subscriptions.views import (
    list_subscription_plan,
    add_subscription_plan,
    update_subscription_plan,
    customer_subscription,
    subscribe_detail,
    subscriptionplan_activate,
    subscriptionplan_deactivate,

)

app_name = "subscriptions"
urlpatterns = [
  path("listSubscriptionPlan/", view=list_subscription_plan, name="listSubscriptionPlan"),
  path("addSubscriptionPlan/", view=add_subscription_plan, name="addSubscriptionPlan"),
  path("updateSubscriptionPlan/<int:pk>", view=update_subscription_plan, name="updateSubscriptionPlan"),
  path('activateSubscriptionPlan/<int:id>', view=subscriptionplan_activate, name='activateSubscriptionPlan'),
  path('deactivateSubscriptionPlan/<int:id>', view=subscriptionplan_deactivate, name='deactivateSubscriptionPlan'),
  path("customerSubscription/", view=customer_subscription, name="customerSubscription"),
  path("subscribe/<int:pk>/", view=subscribe_detail, name="subscribe"),
]