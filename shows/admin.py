"""Admin configuration for shows app."""

from django.contrib import admin
from django.utils.html import format_html

from .models import Actor, Genre, Performance, Show


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin configuration for Genre model."""

    list_display = ("id", "name", "show_count")
    search_fields = ("name",)

    def show_count(self, obj):
        """Return number of shows in this genre."""
        return obj.shows.count()

    show_count.short_description = "Shows Count"


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Admin configuration for Actor model."""

    list_display = ("id", "name", "show_count")
    search_fields = ("name", "bio")
    list_filter = ("shows__genre",)
    fieldsets = (
        (None, {"fields": ("name",)}),
        ("Details", {"fields": ("bio",), "classes": ("collapse",)}),
    )

    def show_count(self, obj):
        """Return number of shows the actor participates in."""
        return obj.shows.count()

    show_count.short_description = "Shows Count"


class PerformanceInline(admin.TabularInline):
    """Inline admin configuration for Performance model."""

    model = Performance
    extra = 1
    fields = ("date_time", "get_bookings_count")
    readonly_fields = ("get_bookings_count",)

    def get_bookings_count(self, obj):
        """Return number of bookings for this performance."""
        if obj.id:
            return obj.bookings.count()
        return 0

    get_bookings_count.short_description = "Bookings"


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    """Admin configuration for Show model."""

    list_display = (
        "id",
        "title",
        "genre",
        "status",
        "get_poster_preview",
        "actor_count",
        "performance_count",
    )
    list_filter = ("status", "genre")
    search_fields = ("title", "genre__name", "actors__name")
    inlines = [PerformanceInline]
    filter_horizontal = ("actors",)
    readonly_fields = ("get_poster_preview",)
    fieldsets = (
        (None, {"fields": ("title", "genre", "status")}),
        (
            "Media",
            {
                "fields": ("poster", "get_poster_preview"),
                "classes": ("collapse",),
            },
        ),
        ("Cast", {"fields": ("actors",)}),
    )

    def get_poster_preview(self, obj):
        """Return HTML with poster preview."""
        if obj.poster:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.poster.url,
            )
        return "No poster"

    get_poster_preview.short_description = "Poster Preview"

    def actor_count(self, obj):
        """Return number of actors in the show."""
        return obj.actors.count()

    actor_count.short_description = "Actors"

    def performance_count(self, obj):
        """Return number of performances scheduled."""
        return obj.performances.count()

    performance_count.short_description = "Performances"


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    """Admin configuration for Performance model."""

    list_display = ("id", "show", "date_time", "get_bookings_count")
    list_filter = ("show", "date_time", "show__genre")
    search_fields = ("show__title",)
    date_hierarchy = "date_time"
    raw_id_fields = ("show",)

    def get_bookings_count(self, obj):
        """Return number of bookings for this performance."""
        return obj.bookings.count()

    get_bookings_count.short_description = "Bookings"
