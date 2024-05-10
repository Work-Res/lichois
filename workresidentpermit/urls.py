
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (ChildCreateListView, EmergencyResPermitApplicationViewSet, EmergencyResidencePermitViewSet,
                    ExemptionCertificateViewSet, ResidencePermitCancellationViewSet,
                    ResidencePermitViewSet, SpouseCreateListView, WorkPermitViewSet,
                    WorkResidentPermitApplicationDetailView, WorkResidentPermitApplicationAPIView,
                    WorkResidentPermitApplicationVerificationAPIView)

router = DefaultRouter()
router.register(r'spouse', SpouseCreateListView, basename='spouse')
router.register(r'child', ChildCreateListView, basename='child')
router.register(r'resident-permit', ResidencePermitViewSet, basename='work-permit-dets')
router.register(r'emergency-res-permit-applications', EmergencyResPermitApplicationViewSet, basename='emergency-permit-apps')
router.register(r'emergency-residence-permits', EmergencyResidencePermitViewSet, basename='emergency-permit')
router.register(r'exemption-certificate', ExemptionCertificateViewSet, basename='exemption-cert')
router.register(r'residence-permit-cancellation', ResidencePermitCancellationViewSet, basename='res-permit-cancellation')
router.register(r'work-permit', WorkPermitViewSet)


urlpatterns = [
    path('workresidentpermit/summary/<str:document_number>', WorkResidentPermitApplicationDetailView.as_view(),
         name='work_resident_permit_detail'),
    path('spouse/<str:document_number>/<str:pk>', SpouseCreateListView.as_view({'get': 'list'}),
         name='spouse-detail'),
    path('workresidentpermit/<str:document_number>/submit', WorkResidentPermitApplicationAPIView.as_view(),
         name='submit-workresident-permit'),
    path('workresidentpermit/<str:document_number>/submit/verification',
         WorkResidentPermitApplicationVerificationAPIView.as_view(), name='submit-verification'),
    path('', include(router.urls)),
]
