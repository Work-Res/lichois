from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app_assessment.views import (
    AssessmentResultViewSet,
    AssessmentViewSet,
    NewAssessmentInvestorViewSet,
    AssessmentEmergencyViewSet,
    RenewalAssessmentInvestorViewSet,
    AppealAssessmentViewSet,
)


router = DefaultRouter()
router.register(r"assessments", AssessmentViewSet)
router.register(r"new_assessment_investors", NewAssessmentInvestorViewSet)
router.register(r"renewal_assessment_investors", RenewalAssessmentInvestorViewSet)
router.register(r"assessment-emergency", AssessmentEmergencyViewSet)
router.register(r"assessment-results", AssessmentResultViewSet)
router.register(r"assessment-appeal", AppealAssessmentViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
