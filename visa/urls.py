from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .admin_site import visa_admin
from .api.viewsets import VisaApplicationViewSet

router = DefaultRouter()


router.register(
    r"visa-applications", VisaApplicationViewSet, basename="visa-applications"
)


urlpatterns = [
    path("admin/", visa_admin.urls),
    path("", include(router.urls)),
]
