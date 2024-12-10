from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChildCreateListView,
    CompleteDeferredApplicationView,
    DeferredApplicationView,
    EmergencyResidencePermitViewSet,
    ExemptionCertificateViewSet,
    PermitAppealViewSet,
    PermitCancellationReasonViewSet,
    PermitCancellationViewSet,
    ResidencePermitViewSet,
    SpouseCreateListView,
    TravelCertificateView,
    WorkPermitApplicationAPIView,
    WorkPermitViewSet,
    WorkResidentPermitApplicationDetailView,
    VariationPermitViewSet,
)

from .admin_site import workresidencepermit_admin

router = DefaultRouter()
router.register(r"spouse", SpouseCreateListView, basename="spouse")
router.register(r"child", ChildCreateListView, basename="child")
router.register(r"resident-permit", ResidencePermitViewSet, basename="resident-permit")
router.register(r"work-permit", WorkPermitViewSet)
router.register(
    r"emergency-permit", EmergencyResidencePermitViewSet, basename="emergency-permit"
)
router.register(
    r"exemption-certificate",
    ExemptionCertificateViewSet,
    basename="exemption-certificate",
)
router.register(
    r"permit-cancellation", PermitCancellationViewSet, basename="permit-cancellation"
)
router.register(r"permit-appeal", PermitAppealViewSet, basename="permit-appeal")
router.register(r"permit-cancellation-reasons", PermitCancellationReasonViewSet)
router.register(r"variation-permit", VariationPermitViewSet)


urlpatterns = [
    
    path('workresidencepermit/', workresidencepermit_admin.urls),
    
    path(
        "spouse/<str:document_number>/<str:pk>",
        SpouseCreateListView.as_view({"get": "list"}),
        name="spouse-detail",
    ),
    # Old endpoints
    path(
        "workpermit/<str:document_number>/submit",
        WorkPermitApplicationAPIView.as_view(),
        name="submit-workresident-permit",
    ),
    path(
        "workresidentpermit/summary/<str:document_number>",
        WorkResidentPermitApplicationDetailView.as_view(),
        name="work_resident_permit_detail",
    ),
    path(
        "production/travel_certificate/<str:document_number>",
        TravelCertificateView.as_view(),
        name="production-permit",
    ),
    path(
        "defer-application/<str:document_number>/",
        DeferredApplicationView.as_view(),
        name="deferred-application",
    ),
    path(
        "deferred-application/<str:document_number>/complete",
        CompleteDeferredApplicationView.as_view(),
        name="deferred-application",
    ),
    path("", include(router.urls)),
]
