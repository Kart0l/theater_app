"""AppConfig for the core app."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """App config for core app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
