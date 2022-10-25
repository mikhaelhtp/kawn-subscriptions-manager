from django.urls import path

from kawn_subscriptions_manager.subscriptions.views import (
    ListSubscriptionPlan,
    AddSubscriptionPlan,
    UpdateSubscriptionPlan,
    DeleteSubscriptionPlan,
    activate_subscription_plan,
    deactivate_subscription_plan,
    ListSubscription,
    AddSubscription,
    ActivateSubscription,
    deactivate_subscription,
)

app_name = "subscriptions"
urlpatterns = [
    path(
        "subscription_plan/list/",
        view=ListSubscriptionPlan.as_view(),
        name="list_subscription_plan",
    ),
    path(
        "subscription_plan/add/",
        view=AddSubscriptionPlan.as_view(),
        name="add_subscription_plan",
    ),
    path(
        "subscription_plan/update/<int:pk>",
        view=UpdateSubscriptionPlan.as_view(),
        name="update_subscription_plan",
    ),
    path(
        "subscription_plan/delete/<int:pk>",
        view=DeleteSubscriptionPlan.as_view(),
        name="delete_subscription_plan",
    ),
    path(
        "subscription_plan/activate/<int:id>",
        view=activate_subscription_plan,
        name="activate_subscription_plan",
    ),
    path(
        "subscription_plan/deactivate/<int:id>",
        view=deactivate_subscription_plan,
        name="deactivate_subscription_plan",
    ),
    path(
        "subscription/list/",
        view=ListSubscription.as_view(),
        name="list_subscription",
    ),
    path(
        "subscription/add/",
        view=AddSubscription.as_view(),
        name="add_subscription",
    ),
    path(
        "subscription/activate/<int:pk>",
        view=ActivateSubscription.as_view(),
        name="activate_subscription",
    ),
    path(
        "subscription/deactivate/<int:id>",
        view=deactivate_subscription,
        name="deactivate_subscription",
    ),
]
