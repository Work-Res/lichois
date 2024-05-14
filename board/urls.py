from django.views.generic.base import RedirectView
from .admin_site import board_admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (AgendaViewSet, AgendaItemViewSet, BoardMeetingViewSet, ApplicationBatchViewSet,
                       MeetingAttendeeViewSet, BoardMeetingVoteViewSet, BoardDecisionViewSet,
                       InterestDeclarationViewSet, MeetingInvitationViewSet)
app_name = 'board'
router = DefaultRouter()
router.register(r'agendas', AgendaViewSet, basename='agendas')
router.register(r'agenda-items', AgendaItemViewSet, basename='agenda-items')
router.register(r'board-meetings', BoardMeetingViewSet, basename='board-meetings')
router.register(r'application-batches', ApplicationBatchViewSet, basename='application-batches')
router.register(r'meeting-attendees', MeetingAttendeeViewSet, basename='meeting-attendees')
router.register(r'board-decision-votes', BoardMeetingVoteViewSet, basename='board-decision-votes')
router.register(r'board-decisions', BoardDecisionViewSet, basename='board-decisions')
router.register(r'interest-declarations', InterestDeclarationViewSet, basename='interest-declarations')
router.register(r'meeting_invitations', MeetingInvitationViewSet, basename='meeting-invitations')


urlpatterns = [
    path('admin/', board_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
    path('', include(router.urls)),
]

