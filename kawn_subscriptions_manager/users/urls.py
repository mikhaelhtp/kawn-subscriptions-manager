from django.urls import path
from .views import (
    UserUpdateView,
    UserDetailView,
    UserRedirectView,
    AddUsers,
    EditUsers,
    DeleteUsers,
    ListUsers,
    profile,
)

app_name = "users"
urlpatterns = [
    # path("invite_users/", invite, name="inviteUsers"),
    path("profile/", profile, name="profile_users"),
    path("list/", ListUsers.as_view(), name="list_users"),
    path("add/", AddUsers.as_view(), name="add_users"),
    path("edit/<int:pk>", EditUsers.as_view(), name="edit_users"),
    path("delete/<int:pk>", DeleteUsers.as_view(), name="delete_users"),
    path("redirect/", UserRedirectView.as_view(), name="redirect"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("<str:username>/", UserDetailView.as_view(), name="detail"),
]
