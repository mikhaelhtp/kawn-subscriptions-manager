from django.db import models
from django.utils.translation import gettext_lazy as _

from kawn_subscriptions_manager.users.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    business_name = models.CharField(_("Business Name"), max_length=255)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)