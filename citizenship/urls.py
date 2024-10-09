from django.urls import path, include
from django.urls.conf import path
from rest_framework.routers import DefaultRouter

from .admin_site import citizenship_admin
from .views.assessment_decision_api_view import AssessmentDecisionAPIView
from .views.board import (
    BoardModelViewSet,
    MeetingViewSet,
    ScoreSheetViewSet,
    MeetingSessionViewSet,
    ConflictOfInterestViewSet,
    ConflictOfInterestDurationViewSet,
    BatchModelViewSet,
    InterviewResponseViewSet,
    AttendeeViewSet,
    BoardMemberViewSet,
    BatchApplicationViewSet,
    BoardRecommendationViewSet, InterviewResponseByInterviewAPIView
)

from .views.board.interview_viewset import InterviewViewSet
from .views.board.scoresheet_attachment_document_viewset import ScoresheetAttachmentDocumentView
from .views.citizenship_minister_decision_api_view import CitizenshipMinisterDecisionAPIView
from .views.citizenship_minister_decision_viewset import CitizenshipMinisterDecisionViewSet
from .views.download_renunciation_attachment_view import DownloadRenunciationAttachmentView
from .views.oath_of_allegiance_viewset import OathOfAllegianceViewSet
from .views.recommendation_decision_api_view import RecommendationDecisionAPIView
from .views.review_decision_api_view import ReviewDecisionAPIView
from .views.summary import (
    RenunciationSummaryViewSet,
    AdoptedChildSummaryViewSet,
    PresPower10ASummaryViewSet,
    PresPower10BSummaryViewSet,
    IntentionNaturalizationFSSummaryViewSet,
    MaturityPeriodWaiverSummaryViewSet,
    DualRenunciationSummaryViewSet,
    SettlementViewSet,
    Under20SummaryViewSet,
    ResumptionSummaryViewSet,
    CertificateInCaseOfDoubtSummaryViewSet,
    FSNaturalizationSummaryViewSet,
    NaturalizationSummaryViewSet
)

app_name = "citizenship"

router = DefaultRouter()
router.register(r"citizenship-boards", BoardModelViewSet)
router.register(r"citizenship-meetings", MeetingViewSet, basename="meeting")
router.register(r"citizenship-meeting-sessions", MeetingSessionViewSet)
router.register(r"citizenship-scoresheets", ScoreSheetViewSet)
router.register(r"citizenship-conflict-of-interests", ConflictOfInterestViewSet)
router.register(
    r"citizenship-conflict-of-interest-durations", ConflictOfInterestDurationViewSet
)
router.register(r"citizenship-batches", BatchModelViewSet, basename="batch")
router.register(r"citizenship-interview-responses", InterviewResponseViewSet)
router.register(r"citizenship-meeting-attendees", AttendeeViewSet)
router.register(r"citizenship-boardmembers", BoardMemberViewSet),
router.register(r"citizenship-batch-applications", BatchApplicationViewSet)
router.register(r"citizenship-interviews", InterviewViewSet, basename="interview")
router.register(r"citizenship-oath-of-allegiance", OathOfAllegianceViewSet, basename="oath-of-allegiance")

router.register(
    r"citizenship-renunciation-summary",
    RenunciationSummaryViewSet,
    basename="renunciation",
)
router.register(
    r"citizenship-adopted-child-summary",
    AdoptedChildSummaryViewSet,
    basename="adopted-child",
)
router.register(
    r"citizenship-pre-10a-summary", PresPower10ASummaryViewSet, basename="pre-10a"
)
router.register(
    r"citizenship-pre-10b-summary", PresPower10BSummaryViewSet, basename="pre-10b"
)
router.register(
    r"citizenship-intention-naturalization",
    IntentionNaturalizationFSSummaryViewSet,
    basename="intention-naturalization",
)
router.register(
    r"citizenship-maturity-waiver",
    MaturityPeriodWaiverSummaryViewSet,
    basename="maturity-waiver",
)

router.register(
    r"citizenship-dual-renunciation",
    DualRenunciationSummaryViewSet,
    basename="dual-renunciation",
)

router.register(
    r"citizenship-resumption",
    ResumptionSummaryViewSet,
    basename="resumption",
)

router.register(
    r"citizenship-certificate-indoubt",
    CertificateInCaseOfDoubtSummaryViewSet,
    basename="certificate-in-doubt",
)

router.register(
    r"citizenship-settlement",
    SettlementViewSet,
    basename="dual-settlement",
)

router.register(
    r"citizenship-under-20-registration",
    Under20SummaryViewSet,
    basename="under-20-summary",
)

router.register(
    r"citizenship-naturalization-fs",
    FSNaturalizationSummaryViewSet,
    basename="naturalization-foreign-spouse",
)

router.register(
    r"citizenship-naturalization",
    NaturalizationSummaryViewSet,
    basename="naturalization",
)

router.register(r'citizenship-minister-decisions', CitizenshipMinisterDecisionViewSet)

router.register(
    r"citizenship-board-recommandation",
    BoardRecommendationViewSet,
    basename="board-recommandation",
)

urlpatterns = [
    path("admin/", citizenship_admin.urls),
    path("", include(router.urls)),
    path(
        "citizenship-assessment-decision/",
        AssessmentDecisionAPIView.as_view(),
        name="assessment-decision-create",
    ),
    path(
        "citizenship-recommendation-case-decision/",
        RecommendationDecisionAPIView.as_view(),
        name="recommandation-decision-create",
    ),
    path(
        "citizenship-review-decision/",
        ReviewDecisionAPIView.as_view(),
        name="review-decision-create",
    ),
    path(
        "citizenship-minister-decision/",
        CitizenshipMinisterDecisionAPIView.as_view(),
        name="review-decision-create",
    ),
    path('scoresheet/download/<str:document_number>/',
         ScoresheetAttachmentDocumentView.as_view(),
         name='download_by_number'),
    path('renunciation-attachments/<str:document_number>/download/',
         DownloadRenunciationAttachmentView.as_view(), name='download_attachment'),
    path('interviewresponses/by-interview-and-member/', InterviewResponseByInterviewAPIView.as_view(),
         name='interview-responses-by-interview'),
]
