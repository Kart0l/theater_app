"""Models for the notifications app."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Notification(TimeStampedModel):
    """Model for user notifications."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

    TYPE_CHOICES = [
        (EMAIL, _("Email")),
        (SMS, _("SMS")),
        (PUSH, _("Push Notification")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(_("Type"), max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(_("Title"), max_length=255)
    message = models.TextField(_("Message"))
    is_read = models.BooleanField(_("Read"), default=False)
    sent_at = models.DateTimeField(_("Sent at"), null=True, blank=True)

    class Meta:
        """Meta options for Notification."""

        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created"]

    def __str__(self) -> str:
        """Return string representation of Notification."""
        return f"{self.title} - {self.user.email}"
