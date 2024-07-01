from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app_assessment.views import AssessmentResultViewSet, AssessmentViewSet, AssessmentInvestorViewSet


router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet)
router.register(r'assessment_investors', AssessmentInvestorViewSet)
router.register(r'assessment-results', AssessmentResultViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
