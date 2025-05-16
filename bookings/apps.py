"""AppConfig for the bookings app."""

from django.apps import AppConfig


class BookingsConfig(AppConfig):
    """App config for bookings app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "bookings"
