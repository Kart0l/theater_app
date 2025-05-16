"""Models for the halls app."""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Hall(TimeStampedModel):
    """Model for theater halls."""

    name = models.CharField(_("Name"), max_length=255)
    capacity = models.PositiveIntegerField(
        _("Capacity"),
        validators=[MinValueValidator(1)],
    )
    description = models.TextField(_("Description"), blank=True)
    schema = models.JSONField(_("Seating Schema"), default=dict)

    class Meta:
        """Meta options for Hall."""

        verbose_name = _("Hall")
        verbose_name_plural = _("Halls")
        ordering = ["name"]

    def __str__(self) -> str:
        """Return string representation of Hall."""
        return f"{self.name} ({self.capacity} seats)"
