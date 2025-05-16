"""Models for the payments app."""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Payment(TimeStampedModel):
    """Model for payment transactions."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

    STATUS_CHOICES = [
        (PENDING, _("Pending")),
        (COMPLETED, _("Completed")),
        (FAILED, _("Failed")),
        (REFUNDED, _("Refunded")),
    ]

    booking = models.OneToOneField(
        "bookings.Booking",
        verbose_name=_("Booking"),
        on_delete=models.CASCADE,
        related_name="payment",
    )
    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    transaction_id = models.CharField(
        _("Transaction ID"), max_length=255, unique=True
    )
    payment_method = models.CharField(_("Payment Method"), max_length=50)

    class Meta:
        """Meta options for Payment."""

        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ["-created"]

    def __str__(self) -> str:
        """Return string representation of Payment."""
        return f"Payment {self.transaction_id} - {self.booking.id}"
