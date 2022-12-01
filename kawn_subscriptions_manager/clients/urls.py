from django.urls import path

from .views import (
    ListClient,
    AddClient,
    UpdateClient,
    DeleteClient,
    ListOutletClient,
    AddOutletClient,
    UpdateOutletClient,
    ListOutlet,
    AddOutlet,
    UpdateOutlet,
    DeleteOutlet,
    load_cities,
)


app_name = "clients"
urlpatterns = [
    path("list/", ListClient.as_view(), name="list_client"),
    path("add/", AddClient.as_view(), name="add_client"),
    path("update/<slug:slug>/", UpdateClient.as_view(), name="update_client"),
    path("delete/<slug:slug>/", DeleteClient.as_view(), name="delete_client"),
    path("outlet-client/list/<slug:slug>/", ListOutletClient.as_view(), name="list_outlet_client"),
    path("outlet-client/add/<slug:slug>/", AddOutletClient.as_view(), name="add_outlet_client"),
    path("outlet-client/update/<slug:slug>/", UpdateOutletClient.as_view(), name="update_outlet_client"),
    path("outlet/list/", ListOutlet.as_view(), name="list_outlet"),
    path("outlets/add/", AddOutlet.as_view(), name="add_outlet"),
    path("outlet/update/<slug:slug>/", UpdateOutlet.as_view(), name="update_outlet"),
    path("outlet/delete/<slug:slug>/", DeleteOutlet.as_view(), name="delete_outlet"),
    path("ajax/load-cities/", load_cities, name="ajax_load_cities"),
]
