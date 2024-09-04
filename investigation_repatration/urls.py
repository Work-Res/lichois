from rest_framework.routers import DefaultRouter

from .views import PrisonerViewSet, PrisonerReleaseLogView, CommitalWarrentViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"prisoners", PrisonerViewSet)
router.register(r"commital-warrent", CommitalWarrentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "prisoner-release-log/",
        PrisonerReleaseLogView.as_view(),
        name="prisoner-release-log",
    ),
]
