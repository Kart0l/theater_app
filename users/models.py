"""Models for the users app."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(_("Email address"), unique=True)
    phone = models.CharField(_("Phone number"), max_length=20, blank=True)
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)

    class Meta:
        """Meta options for User."""

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        """Return string representation of User."""
        return self.email
