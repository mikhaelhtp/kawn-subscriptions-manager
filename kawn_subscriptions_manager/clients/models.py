from tokenize import blank_re
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from kawn_subscriptions_manager.users.models import User



class Account(models.Model):


    class Registered_Via(models.TextChoices):
        WEB = "web", "Web"
        MOBILE_LITE = "mobile_lite", "Mobile Lite"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(_("Name"), max_length=255, null=True)
    address = models.CharField(_("Address"), max_length=255, null=True)
    phone = PhoneNumberField(_("Phone Number"),null=True, unique=True)
    business_code =  models.CharField(_("Business Code"), max_length=255, null=True)
    brand_name = models.CharField(_("Brand Name"), max_length=255, null=True, blank=True)
    brand_logo = models.CharField(_("Brand logo"), max_length=255, null=True)
    social_facebook = models.CharField(_("Facebook"), max_length=255, null=True, blank=True)
    social_twitter = models.CharField(_("Twitter"), max_length=255, null=True, blank=True)
    social_instagram = models.CharField(_("Instagram"), max_length=255, null=True, blank=True)
    website = models.CharField(_("Website"), max_length=255, null=True, blank=True)
    registered_via = models.CharField(_("Registered Via"), max_length=255, choices=Registered_Via.choices, null=True)


class Outlet(models.Model):
    name = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=255, null=True)
    subscription_plan_read = models.CharField(max_length=255, null=True)
    phone = PhoneNumberField(null=True)
    province_read = models.CharField(max_length=255, null=True)
    city_read = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    outlet_code = models.CharField(max_length=10, null=True)
    outlet_image = models.TextField(null=True)
    is_expired = models.BooleanField(null=True)
    transaction_code_prefix = models.CharField(max_length=255, null=True)
    archieved = models.BooleanField(null=True)
    deleted = models.CharField(max_length=255, null=True)
    taxes = models.CharField(max_length=255, null=True)
    gratuity = models.CharField(max_length=255, null=True)
    enable_dashboard = models.BooleanField(null=True)
    branch_id = models.CharField(max_length=255, null=True)
    device_users = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    province = models.IntegerField(null=True)
    city = models.IntegerField(null=True)