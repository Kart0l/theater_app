"""Models for the bookings app."""

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Booking(TimeStampedModel):
    """Model for show bookings."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, _("Pending")),
        (CONFIRMED, _("Confirmed")),
        (CANCELLED, _("Cancelled")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True,
    )
    show = models.ForeignKey(
        "shows.Show",
        verbose_name=_("Show"),
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    hall = models.ForeignKey(
        "halls.Hall",
        verbose_name=_("Hall"),
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    seats = models.JSONField(_("Selected Seats"))
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    total_price = models.DecimalField(
        _("Total Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        """Meta options for Booking."""

        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        ordering = ["-created"]

    def __str__(self) -> str:
        """Return string representation of Booking."""
        user_email = self.user.email if self.user else "Anonymous"
        return f"Booking {self.id} - {user_email} - {self.show.title}"
