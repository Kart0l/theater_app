"""Tests for shows models."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from shows.models import Actor, Genre, Performance, Show


@pytest.mark.django_db
class TestGenre:
    """Test Genre model."""

    def test_genre_creation(self):
        """Test genre can be created."""
        genre = Genre.objects.create(name="Drama")
        assert genre.name == "Drama"
        assert str(genre) == "Drama"


@pytest.mark.django_db
class TestActor:
    """Test Actor model."""

    def test_actor_creation(self):
        """Test actor can be created."""
        actor = Actor.objects.create(
            name="John Doe", bio="Famous theater actor"
        )
        assert actor.name == "John Doe"
        assert actor.bio == "Famous theater actor"
        assert str(actor) == "John Doe"


@pytest.mark.django_db
class TestShow:
    """Test Show model."""

    @pytest.fixture
    def genre(self):
        """Create test genre."""
        return Genre.objects.create(name="Drama")

    @pytest.fixture
    def actor(self):
        """Create test actor."""
        return Actor.objects.create(name="John Doe")

    @pytest.fixture
    def test_image(self):
        """Create test image file."""
        return SimpleUploadedFile(
            name="test_image.jpg",
            content=b"file_content",
            content_type="image/jpeg",
        )

    def test_show_creation(self, genre, actor, test_image):
        """Test show can be created."""
        show = Show.objects.create(
            title="Hamlet",
            genre=genre,
            poster=test_image,
            status=Show.Status.ACTIVE,
        )
        show.actors.add(actor)

        assert show.title == "Hamlet"
        assert show.genre == genre
        assert show.status == Show.Status.ACTIVE
        assert actor in show.actors.all()
        assert str(show) == "Hamlet"

    def test_show_status_choices(self, genre, test_image):
        """Test show status choices."""
        show = Show.objects.create(
            title="Hamlet",
            genre=genre,
            poster=test_image,
            status=Show.Status.ACTIVE,
        )
        assert show.status in [status[0] for status in Show.Status.choices]

        show.status = Show.Status.ARCHIVED
        show.save()
        assert show.status == Show.Status.ARCHIVED


@pytest.mark.django_db
class TestPerformance:
    """Test Performance model."""

    @pytest.fixture
    def show(self, genre):
        """Create test show."""
        return Show.objects.create(
            title="Hamlet", genre=genre, status=Show.Status.ACTIVE
        )

    @pytest.fixture
    def genre(self):
        """Create test genre."""
        return Genre.objects.create(name="Drama")

    def test_performance_creation(self, show):
        """Test performance can be created."""
        date_time = timezone.now()
        performance = Performance.objects.create(
            show=show, date_time=date_time
        )

        assert performance.show == show
        assert performance.date_time == date_time
        assert (
            str(performance)
            == f"Hamlet @ {date_time.strftime('%Y-%m-%d %H:%M')}"
        )

    def test_performance_ordering(self, show):
        """Test performances are ordered by date_time."""
        date1 = timezone.now()
        date2 = date1 + timezone.timedelta(days=1)
        date3 = date1 + timezone.timedelta(days=2)

        p3 = Performance.objects.create(show=show, date_time=date3)
        p1 = Performance.objects.create(show=show, date_time=date1)
        p2 = Performance.objects.create(show=show, date_time=date2)

        performances = Performance.objects.all()
        assert list(performances) == [p3, p2, p1]
