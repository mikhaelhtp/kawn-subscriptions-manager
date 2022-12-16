from tokenize import blank_re
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from datetime import datetime as dt
import uuid
from phonenumber_field.modelfields import PhoneNumberField

from kawn_subscriptions_manager.users.models import User


class Province(models.Model):
    name = models.CharField(_("Province"), max_length=255, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    name = models.CharField(_("City"), max_length=255, null=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(
        max_length=255, editable=False, default=uuid.uuid4, unique=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(_("Client Name"), max_length=255, null=True)
    address = models.CharField(_("Address"), max_length=255, null=True)
    phone = PhoneNumberField(_("Phone Number"), null=True)
    business_code = models.CharField(
        _("Business Code"), max_length=255, null=True
    )
    brand_name = models.CharField(
        _("Brand Name"), max_length=255, null=True, blank=True
    )
    brand_logo = models.CharField(_("Brand logo"), max_length=255, null=True)
    social_facebook = models.CharField(
        _("Facebook"), max_length=255, null=True, blank=True
    )
    social_twitter = models.CharField(
        _("Twitter"), max_length=255, null=True, blank=True
    )
    social_instagram = models.CharField(
        _("Instagram"), max_length=255, null=True, blank=True
    )
    website = models.CharField(_("Website"), max_length=255, null=True, blank=True)
    registered_via = models.CharField(
        max_length=255, default="Kawn Subscriptions Manager"
    )


class Outlet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(
        max_length=255, editable=False, default=uuid.uuid4, unique=True
    )
    name = models.CharField(_("Outlet Name"), max_length=255, null=True)
    display_name = models.CharField(_("Display Name"), max_length=255, null=True)
    subscription_plan_read = models.CharField(max_length=255, null=True)
    phone = PhoneNumberField(_("Phone Number"), null=True)
    province_read = models.CharField(max_length=255, null=True)
    city_read = models.CharField(max_length=255, null=True)
    address = models.CharField(_("Address"), max_length=255, null=True)
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=10,
        validators=[RegexValidator("^[0-9]{5}$", _("Invalid postal code"))],
        null=True,
        blank=True,
    )
    outlet_code = models.CharField(_("Outlet Code"), max_length=10, null=True, blank=True)
    outlet_image = models.URLField(max_length=200, null=True)
    transaction_code_prefix = models.CharField(
        _("Transaction Code Prefix"), max_length=255, null=True, blank=True
    )
    archieved = models.BooleanField(default=True)
    deleted = models.CharField(max_length=255, null=True)
    taxes = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    gratuity = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    enable_dashboard = models.BooleanField(default=True)
    branch_id = models.CharField(max_length=255, null=True)
    device_users = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    province = models.IntegerField(_("Province"), null=True)
    city = models.IntegerField(_("City"), null=True)

    def save(self, *args, **kwargs):
        for field_name in ["transaction_code_prefix", "outlet_code"]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super(Outlet, self).save(*args, **kwargs)
