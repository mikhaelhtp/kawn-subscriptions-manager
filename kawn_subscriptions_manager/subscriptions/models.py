from django.utils import timezone
from django.core.exceptions import ValidationError
from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid

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


class OrderPayment(models.Model):
    class PaymentType(models.TextChoices):
        BANK = "bank_transfer", "Bank Transfer"
        GOPAY = "gopay", "Gopay"
        ECHANEL = "echannel", "Echanel"

    class Status(models.TextChoices):
        EXPIRED = "expired", "Expired"
        CANCELED = "canceled", "Canceled"
        UNPAID = "unpaid", "Unpaid"
        PAID = "paid", "Paid"

    code = models.UUIDField(
        default=uuid.uuid4, unique=True, db_index=True, editable=False
    )
    payment_type = models.CharField(max_length=255, choices=PaymentType.choices)
    amount = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PAID
    )
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)
    modified = models.DateTimeField(auto_now=True)


class SubscriptionDetail(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)
    modified = models.DateTimeField(auto_now=True)
    outlet = models.IntegerField(null=True)
    current_plan = models.IntegerField(null=True)
    choosen_plan = models.IntegerField(null=True)


class Billing(models.Model):
    class Status(models.TextChoices):
        CANCELED = "canceled", "Canceled"
        UNPAID = "unpaid", "Unpaid"
        PAID = "paid", "Paid"

    subscriptiondetail = models.ForeignKey(
        SubscriptionDetail, on_delete=models.CASCADE, null=True
    )
    orderpayment = models.ForeignKey(OrderPayment, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PAID
    )
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)
    modified = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True)
    subscriptionplan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE, null=True
    )
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, null=True)
    expires = models.DateTimeField(null=True)
    billing_date = models.DateTimeField(null=True)
    cancelled = models.BooleanField(null=True)
    voucher = models.IntegerField(null=True)
    active = models.BooleanField(null=True, default=False)
    is_approved = models.BooleanField(null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.JSONField(max_length=255, null=True)
    deleted = models.DateTimeField(null=True)
    deleted_by = models.JSONField(max_length=255, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.JSONField(null=True)

    def clean(self, *args, **kwargs):
        super(Subscription, self).clean(*args, **kwargs)

        if self.expires < timezone.now():
            raise ValidationError("Expires date must be greater than today.")
