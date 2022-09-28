from django.urls import path
from django.contrib import admin
from . import views

from django.views.generic import TemplateView
from kawn_subscriptions_manager.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    add_users,
    list_users,
    edit_users,
    delete_users,
    # invite_users,
    profile,
)

app_name = "users"
urlpatterns = [
    # path("invite_users/", views.invite, name="inviteUsers"),
    path("profile/", profile, name="profile_users"),
    path("add_users/", view=add_users, name="add_users"),
    path("list_users/", view=list_users, name="list_users"),
    path("edit_users/<int:pk>", view=edit_users, name="edit_users"),
    path("delete_users/<int:pk>", view=delete_users, name="delete_users"),
    path("redirect/", view=user_redirect_view, name="redirect"),
    path("update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
