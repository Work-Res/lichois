from rest_framework.routers import DefaultRouter
from .views.prisoner_viewset import PrisonerViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"prisoners", PrisonerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
