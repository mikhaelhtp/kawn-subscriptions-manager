from django.urls import path

from django.views.generic import TemplateView
from kawn_subscriptions_manager.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    add_users,
    profile
)

app_name = "users"
urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='login'),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("addUsers/", view=add_users, name="addUsers"),
    path("profile/", profile, name="users-profile"),
    path("redirect/", view=user_redirect_view, name="redirect"),
    path("update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
