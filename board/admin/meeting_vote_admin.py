from django.contrib import admin
from ..admin_site import board_admin
from ..models import BoardMeetingVote
from ..forms import MeetingVoteForm


@admin.register(BoardMeetingVote, site=board_admin)
class MeetingVoteAdmin(admin.ModelAdmin):
	form = MeetingVoteForm

