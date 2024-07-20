from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .admin_site import visa_admin
from .views import (
    ExemptionCertificateApplicationViewSet,
    ExemptionCertificateViewSet,
    VisaApplicationViewSet,
    VisaViewSet,
)

app_name = "visa"

router = DefaultRouter()

router.register(
    r"exemption-cert-applications",
    ExemptionCertificateApplicationViewSet,
    basename="exemption-cert-applications",
)
router.register(
    r"exemption-certificates",
    ExemptionCertificateViewSet,
    basename="exemption-certificates",
)
router.register(
    r"visa-applications", VisaApplicationViewSet, basename="visa-applications"
)
router.register(r"visas", VisaViewSet, basename="visas")


urlpatterns = [
    path("admin/", visa_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
    path("", include(router.urls)),
]
