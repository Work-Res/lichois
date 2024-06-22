from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TravelCertificateViewSet
from .views import TravelCertificatePermitViewSet

router = DefaultRouter()
router.register(r'travel-certificates', TravelCertificateViewSet)
router.register(r'travel-certificate-permits', TravelCertificatePermitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
