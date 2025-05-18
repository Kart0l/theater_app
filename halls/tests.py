"""Tests for halls app."""

from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from halls.models import Hall, Seat, SeatCategory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def category():
    """Create test seat category."""
    return SeatCategory.objects.create(
        name="VIP",
        description="VIP seats",
        price_modifier=Decimal("1.5"),
        color_code="#FF0000",
    )


@pytest.fixture
def hall():
    """Create test hall."""
    return Hall.objects.create(
        name="Main Hall",
        capacity=100,
        floor=1,
        schema={"rows": 10, "seats_per_row": 10},
        accessibility_features=["wheelchair_access"],
    )


@pytest.fixture
def seat(hall, category):
    """Create test seat."""
    return Seat.objects.create(
        hall=hall,
        category=category,
        row=1,
        number=1,
        coordinates={"x": 10, "y": 20},
    )


class TestSeatCategory:
    """Test suite for SeatCategory model."""

    def test_create_category(self):
        """Test creating a seat category."""
        category = SeatCategory.objects.create(
            name="VIP",
            description="VIP seats with extra comfort",
            price_modifier=Decimal("1.5"),
            color_code="#FF0000",
        )
        assert str(category) == "VIP"
        assert category.price_modifier == Decimal("1.5")

    def test_default_values(self):
        """Test default values for seat category."""
        category = SeatCategory.objects.create(name="Standard")
        assert category.price_modifier == Decimal("1.0")
        assert category.color_code == "#FFFFFF"


class TestHall:
    """Test suite for Hall model."""

    def test_create_hall(self, hall):
        """Test creating a hall."""
        assert str(hall) == "Main Hall (100 seats)"
        assert hall.is_active
        assert hall.is_available

    def test_hall_availability(self, hall):
        """Test hall availability logic."""
        hall.is_active = False
        assert not hall.is_available

        hall.is_active = True
        hall.maintenance_notes = "Under renovation"
        assert not hall.is_available

        hall.maintenance_notes = ""
        assert hall.is_available

    def test_invalid_capacity(self):
        """Test validation of hall capacity."""
        with pytest.raises(ValidationError):
            Hall.objects.create(
                name="Invalid Hall",
                capacity=0,
            )


class TestSeat:
    """Test suite for Seat model."""

    def test_create_seat(self, hall, category):
        """Test creating a seat."""
        seat = Seat.objects.create(
            hall=hall,
            category=category,
            row=1,
            number=1,
            coordinates={"x": 10, "y": 20},
        )
        assert str(seat) == "Main Hall - Row 1, Seat 1"
        assert seat.is_active
        assert seat.is_available

    def test_unique_constraint(self, hall, category):
        """Test unique constraint for seats."""
        Seat.objects.create(
            hall=hall,
            category=category,
            row=1,
            number=1,
        )
        with pytest.raises(IntegrityError):
            Seat.objects.create(
                hall=hall,
                category=category,
                row=1,
                number=1,
            )

    def test_seat_availability(self, hall, category):
        """Test seat availability logic."""
        seat = Seat.objects.create(
            hall=hall,
            category=category,
            row=1,
            number=1,
        )
        assert seat.is_available

        seat.is_active = False
        assert not seat.is_available

        seat.is_active = True
        hall.is_active = False
        hall.save()
        assert not seat.is_available


class TestSeatCategoryViewSet:
    """Test suite for SeatCategoryViewSet."""

    def test_list_categories(self, api_client, category):
        """Test listing seat categories."""
        url = reverse("seatcategory-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == category.name

    def test_create_category(self, api_client):
        """Test creating a seat category."""
        url = reverse("seatcategory-list")
        data = {
            "name": "Standard",
            "description": "Standard seats",
            "price_modifier": "1.0",
            "color_code": "#FFFFFF",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]


class TestHallViewSet:
    """Test suite for HallViewSet."""

    def test_list_halls(self, api_client, hall):
        """Test listing halls."""
        url = reverse("hall-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == hall.name

    def test_create_hall(self, api_client):
        """Test creating a hall."""
        url = reverse("hall-list")
        data = {
            "name": "Small Hall",
            "capacity": 50,
            "floor": 2,
            "schema": {"rows": 5, "seats_per_row": 10},
            "accessibility_features": ["hearing_loop"],
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]

    def test_filter_available_halls(self, api_client, hall):
        """Test filtering halls by availability."""
        url = reverse("hall-list")
        response = api_client.get(f"{url}?is_available=true")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        hall.is_active = False
        hall.save()
        response = api_client.get(f"{url}?is_available=true")
        assert len(response.data) == 0


class TestSeatViewSet:
    """Test suite for SeatViewSet."""

    def test_list_seats(self, api_client, seat):
        """Test listing seats."""
        url = reverse("seat-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["row"] == seat.row
        assert response.data[0]["number"] == seat.number

    def test_create_seat(self, api_client, hall, category):
        """Test creating a seat."""
        url = reverse("seat-list")
        data = {
            "hall": hall.id,
            "category": category.id,
            "row": 2,
            "number": 2,
            "coordinates": {"x": 30, "y": 40},
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["row"] == data["row"]
        assert response.data["number"] == data["number"]

    def test_filter_available_seats(self, api_client, seat):
        """Test filtering seats by availability."""
        url = reverse("seat-list")
        response = api_client.get(f"{url}?is_available=true")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        seat.is_active = False
        seat.save()
        response = api_client.get(f"{url}?is_available=true")
        assert len(response.data) == 0
