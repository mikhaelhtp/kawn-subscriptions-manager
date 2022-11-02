from django.utils import timezone
from django.core.exceptions import ValidationError
from asyncio.windows_events import NULL
from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from kawn_subscriptions_manager.clients.models import Outlet


class SubscriptionPlan(models.Model):
    class Unit(models.TextChoices):
        D = "D", "Day"
        W = "W", "Week"
        M = "M", "Month"
        Y = "Y", "Year"

    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    price = models.FloatField(null=True)
    description = models.TextField(null=True)
    trial_unit = models.CharField(max_length=255, choices=Unit.choices, null=True)
    trial_period = models.SmallIntegerField(null=True)
    recurrence_unit = models.CharField(max_length=255, choices=Unit.choices, null=True)
    recurrence_period = models.SmallIntegerField(null=True)
    is_active = models.BooleanField(null=True, default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self):
        self.slug = slugify(self.name)
        super(SubscriptionPlan, self).save()


class Subscription(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True)
    subscriptionplan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE, null=True
    )
    expires = models.DateTimeField(null=True)
    billing_date = models.DateTimeField(null=True)
    cancelled = models.BooleanField(null=True)
    voucher = models.IntegerField(null=True)
    active = models.BooleanField(null=True, default=False)
    is_approved = models.BooleanField(null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True)
    deleted = models.DateTimeField(null=True)
    deleted_by = models.IntegerField(null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.IntegerField(null=True)

    def clean(self, *args, **kwargs):
        super(Subscription, self).clean(*args, **kwargs)

        if self.expires < timezone.now():
            raise ValidationError("Expires date must be greater than today.")
