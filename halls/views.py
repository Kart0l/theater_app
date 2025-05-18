"""Views for the halls app."""

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Hall, Seat, SeatCategory
from .serializers import HallSerializer, SeatCategorySerializer, SeatSerializer


@extend_schema_view(
    list=extend_schema(
        description="Отримати список категорій місць",
        summary="Список категорій місць",
    ),
    retrieve=extend_schema(
        description="Отримати деталі категорії місць",
        summary="Деталі категорії місць",
    ),
    create=extend_schema(
        description="Створити нову категорію місць",
        summary="Створення категорії місць",
    ),
    update=extend_schema(
        description="Оновити категорію місць",
        summary="Оновлення категорії місць",
    ),
    destroy=extend_schema(
        description="Видалити категорію місць",
        summary="Видалення категорії місць",
    ),
)
class SeatCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for SeatCategory."""

    queryset = SeatCategory.objects.all()
    serializer_class = SeatCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    @method_decorator(cache_page(60 * 5, key_prefix="category_detail"))
    def retrieve(self, request, *args, **kwargs):
        """Return a single category with caching."""
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        """Update a category and invalidate cache."""
        super().perform_update(serializer)
        cache.delete_pattern("*category_detail*")
        cache.delete_pattern("*halls_list*")

    def perform_destroy(self, instance):
        """Delete a category and invalidate cache."""
        super().perform_destroy(instance)
        cache.delete_pattern("*category_detail*")
        cache.delete_pattern("*halls_list*")


@extend_schema_view(
    list=extend_schema(
        description="Отримати список залів",
        summary="Список залів",
    ),
    retrieve=extend_schema(
        description="Отримати деталі залу",
        summary="Деталі залу",
    ),
    create=extend_schema(
        description="Створити новий зал",
        summary="Створення залу",
    ),
    update=extend_schema(
        description="Оновити зал",
        summary="Оновлення залу",
    ),
    destroy=extend_schema(
        description="Видалити зал",
        summary="Видалення залу",
    ),
)
class HallViewSet(viewsets.ModelViewSet):
    """ViewSet for Hall with filtering by status and Redis caching."""

    queryset = Hall.objects.prefetch_related("seats")
    serializer_class = HallSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "capacity", "floor"]
    filterset_fields = ["floor", "is_active"]

    @method_decorator(cache_page(60 * 2, key_prefix="halls_list"))
    def list(self, request, *args, **kwargs):
        """Return a list of halls with caching."""
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5, key_prefix="hall_detail"))
    def retrieve(self, request, *args, **kwargs):
        """Return a single hall with caching."""
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        """Return filtered queryset based on availability."""
        queryset = super().get_queryset()
        is_available = self.request.query_params.get("is_available")
        if is_available is not None:
            is_available = is_available.lower() == "true"
            if is_available:
                queryset = queryset.filter(
                    is_active=True,
                    maintenance_notes="",
                )
            else:
                queryset = queryset.exclude(
                    is_active=True,
                    maintenance_notes="",
                )
        return queryset

    def perform_create(self, serializer):
        """Create a new hall and invalidate cache."""
        super().perform_create(serializer)
        cache.delete_pattern("*halls_list*")

    def perform_update(self, serializer):
        """Update a hall and invalidate cache."""
        super().perform_update(serializer)
        cache.delete_pattern("*halls_list*")
        cache.delete_pattern("*hall_detail*")

    def perform_destroy(self, instance):
        """Delete a hall and invalidate cache."""
        super().perform_destroy(instance)
        cache.delete_pattern("*halls_list*")
        cache.delete_pattern("*hall_detail*")


@extend_schema_view(
    list=extend_schema(
        description="Отримати список місць",
        summary="Список місць",
    ),
    retrieve=extend_schema(
        description="Отримати деталі місця",
        summary="Деталі місця",
    ),
    create=extend_schema(
        description="Створити нове місце",
        summary="Створення місця",
    ),
    update=extend_schema(
        description="Оновити місце",
        summary="Оновлення місця",
    ),
    destroy=extend_schema(
        description="Видалити місце",
        summary="Видалення місця",
    ),
)
class SeatViewSet(viewsets.ModelViewSet):
    """ViewSet for Seat."""

    queryset = Seat.objects.select_related("hall", "category")
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["hall__name", "category__name", "notes"]
    ordering_fields = ["row", "number"]

    def get_queryset(self):
        """Return filtered queryset based on availability."""
        queryset = super().get_queryset()
        is_available = self.request.query_params.get("is_available")
        if is_available is not None:
            is_available = is_available.lower() == "true"
            if is_available:
                queryset = queryset.filter(
                    is_active=True,
                    hall__is_active=True,
                    hall__maintenance_notes="",
                )
            else:
                queryset = queryset.exclude(
                    is_active=True,
                    hall__is_active=True,
                    hall__maintenance_notes="",
                )
        return queryset
