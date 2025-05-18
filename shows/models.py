"""Models for the shows app."""

from django.db import models
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Genre(models.Model):
    """Model representing a genre of theatrical shows."""

    class Meta:
        """Meta options for Genre model."""

        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Return string representation of Genre."""
        return self.name


class Actor(models.Model):
    """Model representing an actor who performs in shows."""

    class Meta:
        """Meta options for Actor model."""

        verbose_name = _("Actor")
        verbose_name_plural = _("Actors")

    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        """Return string representation of Actor."""
        return self.name


class Show(TimeStampedModel):
    """Model representing a theatrical show."""

    class Status(models.TextChoices):
        """Status choices for Show model."""

        ACTIVE = "active", _("Active")
        ARCHIVED = "archived", _("Archived")

    class Meta:
        """Meta options for Show model."""

        verbose_name = _("Show")
        verbose_name_plural = _("Shows")

    title = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="shows",
    )
    actors = models.ManyToManyField(Actor, related_name="shows")
    poster = models.ImageField(upload_to="posters/")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self) -> str:
        """Return string representation of Show."""
        return self.title


class Performance(models.Model):
    """Model representing a scheduled performance of a show."""

    class Meta:
        """Meta options for Performance model."""

        verbose_name = _("Performance")
        verbose_name_plural = _("Performances")
        ordering = ["-date_time"]

    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    date_time = models.DateTimeField()

    def __str__(self) -> str:
        """Return string representation of Performance."""
        if isinstance(self.date_time, str):
            try:
                dt = datetime.fromisoformat(
                    self.date_time.replace("Z", "+00:00")
                )
                return f"{self.show.title} @ {dt.strftime('%Y-%m-%d %H:%M')}"
            except (ValueError, AttributeError):
                return f"{self.show.title} @ {self.date_time}"
        return (
            f"{self.show.title} @ "
            f"{self.date_time.strftime('%Y-%m-%d %H:%M')}"
        )
