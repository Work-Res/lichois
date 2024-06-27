from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app_assessment.views import AssessmentResultViewSet, AssessmentViewSet


router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet)
router.register(r'assessment-results', AssessmentResultViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
