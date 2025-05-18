"""Tests for shows views."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shows.models import Actor, Genre, Performance, Show


@pytest.fixture
def api_client():
    """Create test client."""
    return APIClient()


@pytest.fixture
def genre():
    """Create test genre."""
    return Genre.objects.create(name="Drama")


@pytest.fixture
def actor():
    """Create test actor."""
    return Actor.objects.create(name="John Doe", bio="Famous actor")


@pytest.fixture
def test_image():
    """Create test image file."""
    return SimpleUploadedFile(
        name="test_image.jpg",
        content=b"file_content",
        content_type="image/jpeg",
    )


@pytest.fixture
def show(genre, actor, test_image):
    """Create test show."""
    show = Show.objects.create(
        title="Hamlet",
        genre=genre,
        poster=test_image,
        status=Show.Status.ACTIVE,
    )
    show.actors.add(actor)
    return show


@pytest.mark.django_db
class TestGenreViewSet:
    """Test GenreViewSet."""

    def test_list_genres(self, api_client, genre):
        """Test listing genres."""
        url = reverse("genre-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == genre.name

    def test_create_genre(self, api_client):
        """Test creating genre."""
        url = reverse("genre-list")
        data = {"name": "Comedy"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Comedy"
        assert Genre.objects.count() == 1


@pytest.mark.django_db
class TestActorViewSet:
    """Test ActorViewSet."""

    def test_list_actors(self, api_client, actor):
        """Test listing actors."""
        url = reverse("actor-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == actor.name

    def test_create_actor(self, api_client):
        """Test creating actor."""
        url = reverse("actor-list")
        data = {"name": "Jane Doe", "bio": "Talented actress"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Jane Doe"
        assert Actor.objects.count() == 1


@pytest.mark.django_db
class TestShowViewSet:
    """Test ShowViewSet."""

    def test_list_shows(self, api_client, show):
        """Test listing shows."""
        url = reverse("show-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == show.title

    def test_create_show(self, api_client, genre, actor, test_image):
        """Test creating show."""
        url = reverse("show-list")
        data = {
            "title": "Macbeth",
            "genre": genre.id,
            "actors": [actor.id],
            "poster": test_image,
            "status": Show.Status.ACTIVE,
        }
        response = api_client.post(url, data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Macbeth"
        assert Show.objects.count() == 1

    def test_filter_shows_by_status(self, api_client, show):
        """Test filtering shows by status."""
        url = reverse("show-list")
        response = api_client.get(f"{url}?status={show.status}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == show.status

    def test_search_shows(self, api_client, show):
        """Test searching shows."""
        url = reverse("show-list")
        response = api_client.get(f"{url}?search={show.title}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == show.title


@pytest.mark.django_db
class TestPerformanceViewSet:
    """Test PerformanceViewSet."""

    @pytest.fixture
    def performance(self, show):
        """Create test performance."""
        return Performance.objects.create(
            show=show, date_time="2024-03-01T19:00:00Z"
        )

    def test_list_performances(self, api_client, performance):
        """Test listing performances."""
        url = reverse("performance-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["show"] == performance.show.id

    def test_create_performance(self, api_client, show):
        """Test creating performance."""
        url = reverse("performance-list")
        data = {"show": show.id, "date_time": "2024-03-01T19:00:00Z"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["show"] == show.id
        assert Performance.objects.count() == 1
