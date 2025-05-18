"""URL configuration for the shows app."""

from rest_framework.routers import DefaultRouter

from .views import ActorViewSet, GenreViewSet, PerformanceViewSet, ShowViewSet

app_name = "shows"

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("actors", ActorViewSet, basename="actor")
router.register("shows", ShowViewSet, basename="show")
router.register("performances", PerformanceViewSet, basename="performance")

urlpatterns = router.urls
