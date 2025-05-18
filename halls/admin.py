"""Admin interface for halls app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from halls.models import Hall, Seat, SeatCategory


@admin.register(SeatCategory)
class SeatCategoryAdmin(admin.ModelAdmin):
    """Admin interface for SeatCategory model."""

    list_display = ["name", "price_modifier", "color_code"]
    search_fields = ["name", "description"]
    list_filter = ["price_modifier"]


class SeatInline(admin.TabularInline):
    """Inline admin interface for Seat model."""

    model = Seat
    extra = 0
    fields = ["row", "number", "category", "is_active", "notes"]
    raw_id_fields = ["category"]


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    """Admin interface for Hall model."""

    list_display = ["name", "capacity", "floor", "is_active", "is_available"]
    list_filter = ["is_active", "floor"]
    search_fields = ["name", "description"]
    readonly_fields = ["is_available"]
    fieldsets = [
        (None, {"fields": ["name", "capacity", "floor", "description"]}),
        (
            _("Availability"),
            {"fields": ["is_active", "maintenance_notes", "is_available"]},
        ),
        (
            _("Configuration"),
            {
                "fields": ["schema", "accessibility_features"],
                "classes": ["collapse"],
            },
        ),
    ]
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    """Admin interface for Seat model."""

    list_display = ["__str__", "category", "is_active", "is_available"]
    list_filter = ["hall", "category", "is_active", "row"]
    search_fields = ["hall__name", "notes"]
    raw_id_fields = ["hall", "category"]
    readonly_fields = ["is_available"]
    fieldsets = [
        (None, {"fields": ["hall", "row", "number", "category"]}),
        (_("Status"), {"fields": ["is_active", "is_available", "notes"]}),
        (_("Schema"), {"fields": ["coordinates"], "classes": ["collapse"]}),
    ]
