from django.urls import path

from kawn_subscriptions_manager.subscriptions.views import (
    ListSubscriptionPlan,
    AddSubscriptionPlan,
    UpdateSubscriptionPlan,
    DeleteSubscriptionPlan,
    activate_subscription_plan,
    deactivate_subscription_plan,
    ListSubscription,
    DetailSubscription,
    AddSubscription,
    deactivate_subscription,
    ActivateSubscription,
    SubscriptionLogs,
    ActivityLogsCreated,
    ActivityLogsModified,
    DetailBilling,
    ListApprovalRequest,
    DetailApprovalRequest,
    accept_subscription,
    decline_subscription,
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
    # path(
    #     "logs/",
    #     view=SubscriptionLogs.as_view(),
    #     name="subscription_logs",
    # ),
    path(
        "activity/logs/created/",
        view=ActivityLogsCreated.as_view(),
        name="activity_logs_created",
    ),
    path(
        "activity/logs/modified/",
        view=ActivityLogsModified.as_view(),
        name="activity_logs_modified",
    ),
    path(
        "list/",
        view=ListSubscription.as_view(),
        name="list_subscription",
    ),
    path("detail/<int:pk>", DetailSubscription.as_view(), name="detail_subscription"),
    path(
        "add/",
        view=AddSubscription.as_view(),
        name="add_subscription",
    ),
    path(
        "sales/deactivate/<int:id>",
        view=deactivate_subscription,
        name="deactivate_subscription",
    ),
    path(
        "activate/<int:pk>",
        view=ActivateSubscription.as_view(),
        name="activate_subscription",
    ),
    path(
        "approval/list/",
        view=ListApprovalRequest.as_view(),
        name="list_approval",
    ),
    path(
        "approval/detail/<int:pk>",
        DetailApprovalRequest.as_view(),
        name="detail_approval",
    ),
    path(
        "approval/accept/<int:id>",
        view=accept_subscription,
        name="accept_subscription",
    ),
    path(
        "approval/decline/<int:id>",
        view=decline_subscription,
        name="decline_subscription",
    ),
]
