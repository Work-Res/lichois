from django.urls import path, include
from django.urls.conf import path
from rest_framework.routers import DefaultRouter

from .admin_site import citizenship_admin
from .views.board import (BoardModelViewSet, MeetingViewSet, ScoreSheetViewSet, MeetingSessionViewSet, \
                          ConflictOfInterestViewSet, ConflictOfInterestDurationViewSet, BatchModelViewSet,
                          InterviewResponseViewSet, \
                          AttendeeViewSet, BoardMemberViewSet)

app_name = 'citizenship'

router = DefaultRouter()
router.register(r'citizenship-boards', BoardModelViewSet)
router.register(r'citizenship-meetings', MeetingViewSet, basename='meeting')
router.register(r'citizenship-meeting-sessions', MeetingSessionViewSet)
router.register(r'citizenship-scoresheets', ScoreSheetViewSet)
router.register(r'citizenship-conflict-of-interests', ConflictOfInterestViewSet)
router.register(r'citizenship-conflict-of-interest-durations', ConflictOfInterestDurationViewSet)
router.register(r'citizenship-batches', BatchModelViewSet, basename='batch')
router.register(r'citizenship-interview-responses', InterviewResponseViewSet)
router.register(r'citizenship-meeting-attendees', AttendeeViewSet)
router.register(r'citizenship-boardmembers', BoardMemberViewSet),

urlpatterns = [
    path('admin/', citizenship_admin.urls),
    path('', include(router.urls)),
]
