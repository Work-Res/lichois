from django.urls import path, include

from .views import (
    WorkResidentPermitApplicationDetailView, PermitCreateListView, SpouseCreateListView, ChildCreateListView,
    WorkResidencePermitCreateListView, PlaceOfResidenceViewSet, SpousePlaceOfResidenceViewSet, DeclarationViewSet
)
from .views import EmergencyResPermitApplicationViewSet, EmergencyResidencePermitViewSet
from .views import ExemptionCertificateViewSet, ResidencePermitCancellationViewSet, SecurityClearanceViewSet


from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'spouseplaceofresidence', SpousePlaceOfResidenceViewSet, basename='spouseplaceofresidence')
router.register(r'placeofresidence', PlaceOfResidenceViewSet, basename='placeofresidence')
router.register(r'declarations', DeclarationViewSet, basename='declaration')
router.register(r'permits', PermitCreateListView, basename='permits')
router.register(r'spouse', SpouseCreateListView, basename='spouse')
router.register(r'child', ChildCreateListView, basename='child')
router.register(r'workpermitdetails', WorkResidencePermitCreateListView, basename='work-permit-dets')
router.register(r'emergency-res-permit-applications', EmergencyResPermitApplicationViewSet, basename='emergency-permit-apps')
router.register(r'emergency-residence-permits', EmergencyResidencePermitViewSet, basename='emergency-permit')
router.register(r'exemption-certificate', ExemptionCertificateViewSet, basename='exemption-cert')
router.register(r'residence-permit-cancellation', ResidencePermitCancellationViewSet, basename='res-permit-cancellation')
router.register(r'security-clearances', SecurityClearanceViewSet, basename='security-clearance')


urlpatterns = [
    path('workresidentpermit/summary/<str:document_number>', WorkResidentPermitApplicationDetailView.as_view(),
         name='workresidentpermit-detail'),
    path('spouse/<str:document_number>/<str:pk>', SpouseCreateListView.as_view({'get': 'list'}),
         name='spouse-detail'),
    path('', include(router.urls)),
]
