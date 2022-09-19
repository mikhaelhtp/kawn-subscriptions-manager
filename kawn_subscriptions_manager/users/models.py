from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Types(models.TextChoices):
        SALES = "SALES",  "Sales"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        ADMIN = "ADMIN", "Admin"

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.SALES
    )

    """
    Default custom user model for Kawn Subscriptions Manager.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class SubscriptionPlan(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    duration = models.IntegerField(_("Duration"))
    price = models.IntegerField(_("Price"))
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    subscriptionplan = models.ForeignKey(SubscriptionPlan, on_delete = models.CASCADE)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class SalesManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SALES)

class SupervisorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SUPERVISOR)

class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ADMIN)

class SalesMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gadgets = models.TextField()

class Sales(User):
    base_type = User.Types.SALES
    objects = SalesManager()

    class Meta:
        proxy = True

class SupervisorMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    year = models.IntegerField()

class Supervisor(User):
    base_type = User.Types.SUPERVISOR
    objects = SupervisorManager()

    @property
    def more(self):
        return self.supervisormore

    class Meta:
        proxy = True

class AdminMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    year = models.IntegerField()

class Admin(User):
    base_type = User.Types.ADMIN
    objects = AdminManager()

    @property
    def more(self):
        return self.adminmore

    class Meta:
        proxy = True