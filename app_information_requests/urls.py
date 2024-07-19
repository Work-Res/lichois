from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InformationRequestViewSet, InformationMissingRequestViewSet

router = DefaultRouter()
router.register(r'information-requests', InformationRequestViewSet)
router.register(r'information-missing-requests', InformationMissingRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
