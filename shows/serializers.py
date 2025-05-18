"""Serializers for the shows app."""

from rest_framework import serializers

from .models import Actor, Genre, Performance, Show


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:
        """Meta options."""

        model = Genre
        fields = ["id", "name", "description"]


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for Actor model."""

    class Meta:
        """Meta options."""

        model = Actor
        fields = ["id", "name", "bio", "photo"]


class ShowSerializer(serializers.ModelSerializer):
    """Serializer for Show model."""

    genre = GenreSerializer(read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        """Meta options."""

        model = Show
        fields = [
            "id",
            "title",
            "description",
            "duration",
            "genre",
            "actors",
            "poster",
            "status",
            "created_at",
            "updated_at",
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Performance model."""

    show = ShowSerializer(read_only=True)

    class Meta:
        """Meta options."""

        model = Performance
        fields = [
            "id",
            "show",
            "date",
            "time",
            "price",
            "available_seats",
            "created_at",
            "updated_at",
        ]
