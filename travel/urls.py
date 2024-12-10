from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TravelCertificateViewSet
from .admin_site import travel_certificate_admin

router = DefaultRouter()
router.register(r'travel-certificates', TravelCertificateViewSet)

urlpatterns = [
    path("travelcertificate/", travel_certificate_admin.urls),
    path('', include(router.urls)),
]
