from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet, BiometricsViewSet, ContactDetailsViewSet, PassportViewSet, PersonalDetailsViewSet, CombinedView

router = DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'biometrics', BiometricsViewSet)
router.register(r'contact-details', ContactDetailsViewSet)
router.register(r'passports', PassportViewSet)
router.register(r'personal-details', PersonalDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('combined/', CombinedView.as_view(), name='combined-view'),
]
