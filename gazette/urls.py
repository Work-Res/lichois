from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BatchViewSet,
    BatchDecisionViewSet,
    LegalAssessmentViewSet,
    BatchSubmissionViewSet,
)

router = DefaultRouter()
router.register(r"batches", BatchViewSet, basename="batch")
router.register(r"batch-decisions", BatchDecisionViewSet, basename="batch-decision")
router.register(
    r"legal-assessments", LegalAssessmentViewSet, basename="legal-assessment"
)
router.register(
    r"batch-submissions", BatchSubmissionViewSet, basename="batch-submission"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "batches/<uuid:pk>/add_application/",
        BatchViewSet.as_view({"post": "add_application"}),
        name="add_application",
    ),
    path(
        "batches/<uuid:pk>/add_applications/",
        BatchViewSet.as_view({"post": "add_applications"}),
        name="add_applications",
    ),
    path(
        "batches/<uuid:pk>/remove_application/",
        BatchViewSet.as_view({"post": "remove_application"}),
        name="remove_application",
    ),
    path(
        "batches/<uuid:pk>/submit/",
        BatchViewSet.as_view({"post": "submit_batch"}),
        name="submit_batch",
    ),
    path(
        "batches/<uuid:pk>/create_decision/",
        BatchViewSet.as_view({"post": "create_batch_decision"}),
        name="create_batch_decision",
    ),
    path(
        "batch-submissions/<uuid:pk>/submit/",
        BatchSubmissionViewSet.as_view({"post": "submit_batch"}),
        name="submit_batch_submission",
    ),
    path(
        "batch-submissions/<uuid:pk>/update_status/",
        BatchSubmissionViewSet.as_view({"post": "update_batch_status"}),
        name="update_batch_status_submission",
    ),
]
