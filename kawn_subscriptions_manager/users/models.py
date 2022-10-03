from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

UNIQUE_EMAIL = getattr(settings, "ACCOUNT_UNIQUE_EMAIL", True)
EMAIL_MAX_LENGTH = getattr(settings, "ACCOUNT_EMAIL_MAX_LENGTH", 254)


class User(AbstractUser):
    class Types(models.TextChoices):
        SALES = "SALES", "Sales"
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
    email = models.EmailField(
        unique=UNIQUE_EMAIL, max_length=EMAIL_MAX_LENGTH, verbose_name="e-mail address"
    )
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})