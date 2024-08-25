from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api.viewsets import PermanentResidenceViewSet

router = DefaultRouter()


router.register(
    r"permanent-residence", PermanentResidenceViewSet, basename="permanent-residence"
)


urlpatterns = [
    path("", include(router.urls)),
]
