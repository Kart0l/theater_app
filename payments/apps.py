"""AppConfig for the payments app."""

from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    """App config for payments app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "payments"
