"""Models for the shows app."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Show(TimeStampedModel):
    """Model for theater shows."""

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    duration = models.DurationField(_("Duration"))
    poster = models.ImageField(
        _("Poster"), upload_to="shows/posters/", null=True, blank=True
    )

    class Meta:
        """Meta options for Show."""

        verbose_name = _("Show")
        verbose_name_plural = _("Shows")
        ordering = ["-created"]

    def __str__(self) -> str:
        """Return string representation of Show."""
        return self.title
