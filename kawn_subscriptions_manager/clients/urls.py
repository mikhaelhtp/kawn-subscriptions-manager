from django.urls import path

from kawn_subscriptions_manager.clients.views import list_client, add_client, delete_client

app_name = 'clients'
urlpatterns = [
    path("list_client/", view=list_client, name="list_client"),
    path("add_client/", view=add_client, name="add_client"),
    path('delete_client/<int:pk>/', view=delete_client, name='delete_client'),
]