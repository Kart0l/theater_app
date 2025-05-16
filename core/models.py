"""Models for the core app."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Base model with created and modified timestamps."""

    created = models.DateTimeField(
        _("Created"), auto_now_add=True, db_index=True
    )
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    class Meta:
        """Meta options for TimeStampedModel."""

        abstract = True
