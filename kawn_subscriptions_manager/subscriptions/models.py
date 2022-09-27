from django.db import models
from kawn_subscriptions_manager.clients.models import Client
from django.utils.translation import gettext_lazy as _

# Create your models here.
class SubscriptionPlan(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    duration = models.IntegerField(_("Duration"))
    price = models.IntegerField(_("Price"))
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete = models.CASCADE, null=True)
    subscriptionplan = models.ForeignKey(SubscriptionPlan, on_delete = models.CASCADE)
    start_date = models.DateTimeField(_("Start Date") )
    end_date = models.DateTimeField(_("End Date"))
    price = models.IntegerField(_("Price"), null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def subscription_price(self):
        return self.subscriptionplan.price
