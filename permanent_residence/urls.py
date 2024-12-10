from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api.viewsets import PermanentResidenceViewSet

from .admin_site import permanent_residence_admin

router = DefaultRouter()


router.register(
    r"permanent-residence", PermanentResidenceViewSet, basename="permanent-residence"
)


urlpatterns = [
    
    path("permanentresidence/", permanent_residence_admin.urls),
    path("", include(router.urls)),
]
