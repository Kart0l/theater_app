"""Serializers for the halls app."""

from rest_framework import serializers

from .models import Hall, Seat, SeatCategory


class SeatCategorySerializer(serializers.ModelSerializer):
    """Serializer for SeatCategory model."""

    class Meta:
        """Meta options."""

        model = SeatCategory
        fields = [
            "id",
            "name",
            "description",
            "price_modifier",
            "color_code",
            "created_at",
            "updated_at",
        ]


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat model."""

    category = SeatCategorySerializer(read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        """Meta options."""

        model = Seat
        fields = [
            "id",
            "hall",
            "category",
            "row",
            "number",
            "is_active",
            "notes",
            "coordinates",
            "is_available",
            "created_at",
            "updated_at",
        ]


class HallSerializer(serializers.ModelSerializer):
    """Serializer for Hall model."""

    seats = SeatSerializer(many=True, read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        """Meta options."""

        model = Hall
        fields = [
            "id",
            "name",
            "capacity",
            "description",
            "schema",
            "is_active",
            "maintenance_notes",
            "floor",
            "accessibility_features",
            "seats",
            "is_available",
            "created_at",
            "updated_at",
        ]
