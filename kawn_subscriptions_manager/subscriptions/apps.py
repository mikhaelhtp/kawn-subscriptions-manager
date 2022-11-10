from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriptionsConfig(AppConfig):
    name = "kawn_subscriptions_manager.subscriptions"
    verbose_name = _("Subscriptions")

    def ready(self):
        try:
            import kawn_subscriptions_manager.users.signals  # noqa F401
        except ImportError:
            pass


class POS(SubscriptionsConfig):
    pass
