"""URLs for the halls app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HallViewSet, SeatCategoryViewSet, SeatViewSet

router = DefaultRouter()
router.register("categories", SeatCategoryViewSet)
router.register("halls", HallViewSet)
router.register("seats", SeatViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
