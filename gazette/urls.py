from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BatchViewSet,
    BatchDecisionViewSet,
    LegalAssessmentViewSet,
    BatchSubmissionViewSet,
    BatchApplicationViewSet,
    DownloadGazettePDFView,
)

router = DefaultRouter()
router.register(r"gazette-batches", BatchViewSet, basename="batch")
router.register(
    r"gazette-batch-decisions", BatchDecisionViewSet, basename="batch-decision"
)
router.register(
    r"gazette-legal-assessments", LegalAssessmentViewSet, basename="legal-assessment"
)
router.register(
    r"gazette-batch-submissions", BatchSubmissionViewSet, basename="batch-submission"
)

router.register(
    r"gazette-batch-applications",
    BatchApplicationViewSet,
    basename="batch-applications",
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "gazette-batches/<uuid:pk>/add_application/",
        BatchViewSet.as_view({"post": "add_application"}),
        name="add_application",
    ),
    path(
        "gazette-batches/<uuid:pk>/add_applications/",
        BatchViewSet.as_view({"post": "add_applications"}),
        name="add_applications",
    ),
    path(
        "gazette-batches/<uuid:pk>/remove_application/",
        BatchViewSet.as_view({"post": "remove_application"}),
        name="remove_application",
    ),
    path(
        "gazette-batches/<uuid:pk>/submit/",
        BatchViewSet.as_view({"post": "submit_batch"}),
        name="submit_batch",
    ),
    path(
        "gazette-batches/<uuid:pk>/create_decision/",
        BatchViewSet.as_view({"post": "create_batch_decision"}),
        name="create_batch_decision",
    ),
    path(
        "gazette-batch-submissions/<uuid:pk>/submit/",
        BatchSubmissionViewSet.as_view({"post": "submit_batch"}),
        name="submit_batch_submission",
    ),
    path(
        "gazette-batch-submissions/<uuid:pk>/update_status/",
        BatchSubmissionViewSet.as_view({"post": "update_batch_status"}),
        name="update_batch_status_submission",
    ),
    path(
        "download-gazette/<uuid:batch_id>/",
        DownloadGazettePDFView.as_view(),
        name='download_gazette_pdf'
    )
]
