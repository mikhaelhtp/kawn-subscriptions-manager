from django.urls import path

from .views import (
    ListClient,
    AddClient,
    UpdateClient,
    DeleteClient,
    activate_client,
    deactivate_client,
)


app_name = "clients"
urlpatterns = [
    path("list_client/", ListClient.as_view(), name="list_client"),
    path("add_client/", AddClient.as_view(), name="add_client"),
    path("update_client/<int:pk>", UpdateClient.as_view(), name="update_client"),
    path("delete_client/<int:pk>/", DeleteClient.as_view(), name="delete_client"),
    path("activate_client/<int:id>", activate_client, name="activate_client"),
    path("deactivate_client/<int:id>", deactivate_client, name="deactivate_client"),
]
