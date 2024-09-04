from rest_framework.routers import DefaultRouter
from .views import PrisonerViewSet, PrisonerReleaseLogViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"prisoners", PrisonerViewSet)
router.register(r"release-log", PrisonerReleaseLogViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
