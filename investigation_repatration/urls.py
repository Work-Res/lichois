from rest_framework.routers import DefaultRouter


from .views import (
    PrisonerViewSet,
    PrisonerReleaseLogView,
    CommitalWarrentViewSet,
    UpdatePrisonerReleaseLogView,
    ProhibitedImmigrantViewSet,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"prisoners", PrisonerViewSet)
router.register(r"commital-warrent", CommitalWarrentViewSet)
router.register(r"prohibited-immigrant", ProhibitedImmigrantViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "prisoner-release-log/",
        PrisonerReleaseLogView.as_view(),
        name="prisoner-release-log",
    ),
    path(
        "prisoner-release-log/<str:id>/",
        UpdatePrisonerReleaseLogView.as_view(),
        name="prisoner-release-log",
    ),
]
