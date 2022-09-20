from django.urls import path
from kawn_subscriptions_manager.subscriptions.views import (
    list_subscription_plan,
    add_subscription_plan,
    edit_subscription_plan,
    list_user_subscription,
    subscribe_detail,
)

app_name = "subscriptions"
urlpatterns = [
  path("listSubscriptionPlan/", view=list_subscription_plan, name="listSubscriptionPlan"),
  path("addSubscriptionPlan/", view=add_subscription_plan, name="addSubscriptionPlan"),
  path("editSubscriptionPlan/", view=edit_subscription_plan, name="editSubscriptionPlan"),
  path("listUserSubscription/", view=list_user_subscription, name="listUserSubscription"),
  path("subscribe/<int:pk>/", view=subscribe_detail, name="subscribe"),
]