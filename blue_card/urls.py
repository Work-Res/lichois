from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .admin_site import blue_card_admin
from .api.viewsets import BlueCardViewSet

router = DefaultRouter()

router.register(r"blue-cards", BlueCardViewSet, basename="blue-cards")

urlpatterns = [
    path("bluecard/", blue_card_admin.urls),
    path("", include(router.urls)),
]
