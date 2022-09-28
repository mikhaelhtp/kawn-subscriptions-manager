from django.urls import path

from kawn_subscriptions_manager.subscriptions.views import (
    ListSubscriptionPlan,
    AddSubscriptionPlan,
    UpdateSubscriptionPlan,
    DeleteSubscriptionPlan,
    activate_subscription_plan,
    deactivate_subscription_plan,
    ListClientSubscription,
    AddClientSubscription,
    UpdateClientSubscription,
    deactivate_client_subscription,
)

app_name = "subscriptions"
urlpatterns = [
    path(
        "list/subscription_plan/",
        view=ListSubscriptionPlan.as_view(),
        name="list_subscription_plan",
    ),
    path(
        "add/subscription_plan/",
        view=AddSubscriptionPlan.as_view(),
        name="add_subscription_plan",
    ),
    path(
        "update/subscription_plan/<int:pk>",
        view=UpdateSubscriptionPlan.as_view(),
        name="update_subscription_plan",
    ),
    path(
        "delete/subscription_plan/<int:pk>",
        view=DeleteSubscriptionPlan.as_view(),
        name="delete_subscription_plan",
    ),
    path(
        "activate/subscription_plan/<int:id>",
        view=activate_subscription_plan,
        name="activate_subscription_plan",
    ),
    path(
        "deactivate/subscription_plan/<int:id>",
        view=deactivate_subscription_plan,
        name="deactivate_subscription_plan",
    ),
    path(
        "list/client_subscription/",
        view=ListClientSubscription.as_view(),
        name="list_client_subscription",
    ),
    path(
        "add/client_subscription/",
        view=AddClientSubscription.as_view(),
        name="add_client_subscription",
    ),
    path(
        "update/client_subscription/<int:pk>",
        view=UpdateClientSubscription.as_view(),
        name="update_client_subscription",
    ),
    path(
        "deactivate/client_subscription/<int:id>",
        view=deactivate_client_subscription,
        name="deactivate_client_subscription",
    ),
]
