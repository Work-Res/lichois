from rest_framework.routers import DefaultRouter


from .views import (
    PrisonerViewSet,
    PrisonerReleaseLogView,
    CommitalWarrentViewSet,
    UpdatePrisonerReleaseLogView,
    ProhibitedImmigrantViewSet,
    PIDeclarationOrderViewSet,
    PIDeclarationOrderAcknowledgementViewSet,
    GetReleaseLogProfilesView,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"prisoners", PrisonerViewSet)
router.register(r"commital-warrent", CommitalWarrentViewSet)
router.register(r"prohibited-immigrant", ProhibitedImmigrantViewSet)
router.register(r"pi-declaration-order", PIDeclarationOrderViewSet)
router.register(
    r"pi-declaration-order-acknowledgement", PIDeclarationOrderAcknowledgementViewSet
)


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
    path(
        "get-release-log-profiles/<str:id>/",
        GetReleaseLogProfilesView.as_view(),
        name="get-release-log-profile",
    ),
]
