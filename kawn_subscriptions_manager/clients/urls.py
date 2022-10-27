from django.urls import path
from . import views

from .views import (
    ListClient,
    AddClient,
    UpdateClient,
    DeleteClient,
    ListOutletClient,
    AddClientOutlet,
    DeleteClientOutlet,
    ListOutlet,
    AddOutlet,
    UpdateOutlet,
    load_cities,
)


app_name = "clients"
urlpatterns = [
    path("list/", ListClient.as_view(), name="list_client"),
    path("add/", AddClient.as_view(), name="add_client"),
    path("update/<int:pk>", UpdateClient.as_view(), name="update_client"),
    path("delete/<int:pk>/", DeleteClient.as_view(), name="delete_client"),
    path("outlet/list/<int:pk>", ListOutletClient.as_view(), name="list_outlet_client"),
    path("outlet/add/<int:pk>", AddClientOutlet.as_view(), name="add_outlet_client"),
    path("outlet/delete/<int:pk>", DeleteClientOutlet, name="delete_outlet_client"),
    path("outlet/list/", ListOutlet.as_view(), name="list_outlet"),
    path("outlets/add/", AddOutlet.as_view(), name="add_outlet"),
    path("outlet/update/<int:pk>/", UpdateOutlet.as_view(), name="update_outlet"),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
