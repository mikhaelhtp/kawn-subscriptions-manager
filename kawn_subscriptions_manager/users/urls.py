from django.urls import path
from .views import (
    UserUpdateView,
    UserDetailView,
    UserRedirectView,
    AddUsers,
    EditUsers,
    deactivate_user,
    activate_user,
    DeleteUsers,
    ListUsers,
    profile,
)

app_name = "users"
urlpatterns = [
    path("profile/", profile, name="profile_users"),
    path("list/", ListUsers.as_view(), name="user_list"),
    path("add/", AddUsers.as_view(), name="add_users"),
    path("edit/<int:pk>", EditUsers.as_view(), name="edit_users"),
    path("deactivate/<int:id>", deactivate_user, name="deactivate_user"),
    path("activate/<int:id>", activate_user, name="activate_user"),
    path("delete/<int:pk>", DeleteUsers.as_view(), name="delete_users"),
    path("redirect/", UserRedirectView.as_view(), name="redirect"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("<str:username>/", UserDetailView.as_view(), name="detail"),
]
