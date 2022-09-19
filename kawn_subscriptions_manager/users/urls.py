from django.urls import path

from django.views.generic import TemplateView
from kawn_subscriptions_manager.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    add_supervisor,
    list_subscription_plan,
    add_subscription_plan,
    edit_subscription_plan,
    list_user_subscription,
    subscribe_detail,
    home,
    profile
)

app_name = "users"
urlpatterns = [
    path('', home, name='home'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path("addSupervisor/", view=add_supervisor, name="addSupervisor"),
    path("listSubscriptionPlan/", view=list_subscription_plan, name="listSubscriptionPlan"),
    path("addSubscriptionPlan/", view=add_subscription_plan, name="addSubscriptionPlan"),
    path("editSubscriptionPlan/", view=edit_subscription_plan, name="editSubscriptionPlan"),
    path("listUserSubscription/", view=list_user_subscription, name="listUserSubscription"),
    path('subscribe/<int:pk>/', view=subscribe_detail, name='subscribe'),
    path('profile/', profile, name='users-profile'),
    path("redirect/", view=user_redirect_view, name="redirect"),
    path("update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
