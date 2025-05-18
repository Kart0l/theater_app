"""Models for the halls app."""

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


def validate_coordinates(value):
    """Validate seat coordinates."""
    if not isinstance(value, dict):
        raise ValidationError(_("Coordinates must be a dictionary"))

    required_keys = {"x", "y"}
    if set(value.keys()) != required_keys:
        raise ValidationError(
            _("Coordinates must contain exactly 'x' and 'y' values")
        )

    for key in required_keys:
        if not isinstance(value[key], (int, float)):
            raise ValidationError(_(f"Coordinate {key} must be a number"))
        if value[key] < 0:
            raise ValidationError(_(f"Coordinate {key} cannot be negative"))


class SeatCategory(TimeStampedModel):
    """Model for seat categories in halls."""

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    price_modifier = models.DecimalField(
        _("Price Modifier"),
        max_digits=5,
        decimal_places=2,
        default=1.0,
        help_text=_("Multiplier for base ticket price"),
    )
    color_code = models.CharField(
        _("Color Code"),
        max_length=7,
        default="#FFFFFF",
        help_text=_("HEX color code for UI representation"),
    )

    class Meta:
        """Meta options for SeatCategory."""

        verbose_name = _("Seat Category")
        verbose_name_plural = _("Seat Categories")
        ordering = ["name"]

    def __str__(self) -> str:
        """Return string representation of SeatCategory."""
        return self.name


class Hall(TimeStampedModel):
    """Model for theater halls."""

    name = models.CharField(_("Name"), max_length=255)
    capacity = models.PositiveIntegerField(
        _("Capacity"),
        validators=[MinValueValidator(1)],
    )
    description = models.TextField(_("Description"), blank=True)
    schema = models.JSONField(
        _("Seating Schema"),
        default=dict,
        help_text=_("JSON schema of hall layout"),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Whether this hall is available for scheduling"),
    )
    maintenance_notes = models.TextField(
        _("Maintenance Notes"),
        blank=True,
        help_text=_("Notes about hall maintenance or issues"),
    )
    floor = models.PositiveSmallIntegerField(
        _("Floor Number"),
        default=1,
    )
    accessibility_features = models.JSONField(
        _("Accessibility Features"),
        default=list,
        help_text=_("List of accessibility features available"),
    )

    class Meta:
        """Meta options for Hall."""

        verbose_name = _("Hall")
        verbose_name_plural = _("Halls")
        ordering = ["name"]

    def __str__(self) -> str:
        """Return string representation of Hall."""
        return f"{self.name} ({self.capacity} seats)"

    @property
    def is_available(self) -> bool:
        """Check if hall is available for scheduling."""
        return self.is_active and not self.maintenance_notes


class Seat(TimeStampedModel):
    """Model for individual seats in halls."""

    hall = models.ForeignKey(
        "halls.Hall",
        verbose_name=_("Hall"),
        on_delete=models.CASCADE,
        related_name="seats",
    )
    category = models.ForeignKey(
        "halls.SeatCategory",
        verbose_name=_("Category"),
        on_delete=models.PROTECT,
        related_name="seats",
    )
    row = models.PositiveSmallIntegerField(_("Row Number"))
    number = models.PositiveSmallIntegerField(_("Seat Number"))
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Whether this seat is available for booking"),
    )
    notes = models.TextField(
        _("Notes"),
        blank=True,
        help_text=_("Additional information about the seat"),
    )
    coordinates = models.JSONField(
        _("Coordinates"),
        default=dict,
        help_text=_("X,Y coordinates for interactive schema"),
        validators=[validate_coordinates],
    )

    class Meta:
        """Meta options for Seat."""

        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")
        ordering = ["hall", "row", "number"]
        unique_together = [["hall", "row", "number"]]

    def __str__(self) -> str:
        """Return string representation of Seat."""
        return f"{self.hall.name} - Row {self.row}, Seat {self.number}"

    @property
    def is_available(self) -> bool:
        """Check if seat is available for booking."""
        return self.is_active and self.hall.is_available

    def clean(self):
        """Validate seat coordinates against hall schema."""
        super().clean()
        if not self.coordinates:
            return

        schema = self.hall.schema
        if not schema:
            return

        max_x = schema.get("seats_per_row", 0) * 50  # Assuming 50px per seat
        max_y = schema.get("rows", 0) * 50  # Assuming 50px per row

        if self.coordinates["x"] > max_x or self.coordinates["y"] > max_y:
            raise ValidationError(
                _(
                    "Seat coordinates (%(x)d, %(y)d) are outside "
                    "the hall bounds (%(max_x)d, %(max_y)d)"
                ),
                params={
                    "x": self.coordinates["x"],
                    "y": self.coordinates["y"],
                    "max_x": max_x,
                    "max_y": max_y,
                },
            )
