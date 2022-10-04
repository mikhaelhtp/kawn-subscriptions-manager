from django.urls import path

from .views import (
    ListClient,
    AddClient,
    UpdateClient,
    DeleteClient,
    activate_client,
    deactivate_client,
    ListOutlet,
    AddOutlet
)


app_name = "clients"
urlpatterns = [
    path("list/", ListClient.as_view(), name="list_client"),
    path("add/", AddClient.as_view(), name="add_client"),
    path("update/<int:pk>/", UpdateClient.as_view(), name="update_client"),
    path("delete/<int:pk>/", DeleteClient.as_view(), name="delete_client"),
    path("activate/<int:id>/", activate_client, name="activate_client"),
    path("deactivate/<int:id>/", deactivate_client, name="deactivate_client"),
    path("outlets/list/<int:id>/", ListOutlet.as_view(), name="list_outlet_client"),
    path("outlets/add/<int:id>", AddOutlet.as_view(), name="add_outlet_client"),
]
