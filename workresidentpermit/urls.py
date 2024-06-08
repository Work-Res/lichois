
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (ChildCreateListView, EmergencyResidencePermitViewSet,
                    ExemptionCertificateViewSet, PermitCancellationViewSet,
                    ResidencePermitViewSet, SpouseCreateListView, WorkPermitViewSet,
                    WorkResidentPermitApplicationDetailView, WorkPermitApplicationAPIView,
                    WorkPermitApplicationVerificationAPIView,
                    SecurityClearanceCreateAPIView)

router = DefaultRouter()
router.register(r'spouse', SpouseCreateListView, basename='spouse')
router.register(r'child', ChildCreateListView, basename='child')
router.register(r'resident-permit', ResidencePermitViewSet, basename='resident-permit')
router.register(r'work-permit', WorkPermitViewSet)
router.register(r'emergency-permit', EmergencyResidencePermitViewSet, basename='emergency-permit')
router.register(r'exemption-certificate', ExemptionCertificateViewSet, basename='exemption-certificate')
router.register(r'permit-cancellation', PermitCancellationViewSet, basename='permit-cancellation')


urlpatterns = [
    path('workresidentpermit/summary/<str:document_number>', WorkResidentPermitApplicationDetailView.as_view(),
         name='work_resident_permit_detail'),
    path('spouse/<str:document_number>/<str:pk>', SpouseCreateListView.as_view({'get': 'list'}),
         name='spouse-detail'),
    path('workpermit/<str:document_number>/submit', WorkPermitApplicationAPIView.as_view(),
         name='submit-workresident-permit'),
    path('workpermit/<str:document_number>/submit/verification',
         WorkPermitApplicationVerificationAPIView.as_view(), name='submit-verification'),
    path('workpermit/<str:document_number>/submit/security_clearance',
         SecurityClearanceCreateAPIView.as_view(), name='submit-security-clearance'),
    path('', include(router.urls)),
]

