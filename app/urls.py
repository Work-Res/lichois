from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app.views import (
    ApplicationListView,
    ApplicationCreateView,
    ApplicationStatusViewSet,
    ApplicationRenewalView,
    ApplicationRenewalHistoryView,
    ApplicationReplacementHistoryView,
    ApplicationVerificationAPIView,
    SecurityClearanceCreateAPIView,
    CommissionerDecisionAPIView,
    MinisterDecisionAPIView,
    RecommendationCaseDecisionAPIView,
    PresRecommendationDecisionAPIView,
    DirectorDecisionAPIView, ApplicationAppealHistoryView
)

router = DefaultRouter()

router.register(r"applications", ApplicationListView)
router.register(r"application_statuses", ApplicationStatusViewSet)
router.register(r"application_renewal_history", ApplicationRenewalHistoryView)
router.register(r"application_appeal_history", ApplicationAppealHistoryView)
router.register(r"application_replacement_history", ApplicationReplacementHistoryView)

urlpatterns = [
    path("applications", ApplicationCreateView.as_view(), name="application-new"),
    path(
        "applications/renewal",
        ApplicationRenewalView.as_view(),
        name="application-renewal",
    ),
    path("", include(router.urls)),
    path(
        "app/verification/<str:document_number>/submit/",
        ApplicationVerificationAPIView.as_view(),
        name="submit-verification",
    ),
    path(
        "security_clearance/<str:document_number>/submit/",
        SecurityClearanceCreateAPIView.as_view(),
        name="submit-security-clearance",
    ),
    path(
        "commissioner-decision/",
        CommissionerDecisionAPIView.as_view(),
        name="commissioner-decision-create",
    ),
    path(
        "recommendation-case-decision/",
        RecommendationCaseDecisionAPIView.as_view(),
        name="recommandation-decision-create",
    ),
    path(
        "minister-decision/",
        MinisterDecisionAPIView.as_view(),
        name="minister-decision-create",
    ),
    path(
        "pres-recommendation-decision/",
        PresRecommendationDecisionAPIView.as_view(),
        name="pres-recommendation-decision-create",
    ),
    path(
        "director-decision/",
        DirectorDecisionAPIView.as_view(),
        name="director-decision-create",
    ),
]
