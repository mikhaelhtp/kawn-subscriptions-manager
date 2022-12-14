from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kawn_subscriptions_manager.clients"

    def ready(self):
        pass