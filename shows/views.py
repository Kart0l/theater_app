"""Views for the shows app."""

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Actor, Genre, Performance, Show
from .serializers import (
    ActorSerializer,
    GenreSerializer,
    PerformanceSerializer,
    ShowSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet for Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ActorViewSet(viewsets.ModelViewSet):
    """ViewSet for Actor."""

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ShowViewSet(viewsets.ModelViewSet):
    """ViewSet for Show with filtering by status and Redis caching."""

    queryset = Show.objects.prefetch_related(
        "actors", "performances"
    ).select_related("genre")
    serializer_class = ShowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "genre__name", "actors__name"]
    ordering_fields = ["title", "status"]

    @method_decorator(cache_page(60 * 2, key_prefix="shows_list"))
    def list(self, request, *args, **kwargs):
        """Return a list of shows with caching."""
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """Return filtered queryset based on status parameter."""
        queryset = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        """Create a new show and invalidate cache."""
        super().perform_create(serializer)
        cache.delete_pattern("*shows_list*")

    def perform_update(self, serializer):
        """Update a show and invalidate cache."""
        super().perform_update(serializer)
        cache.delete_pattern("*shows_list*")

    def perform_destroy(self, instance):
        """Delete a show and invalidate cache."""
        super().perform_destroy(instance)
        cache.delete_pattern("*shows_list*")


class PerformanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Performance."""

    queryset = Performance.objects.select_related("show")
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
