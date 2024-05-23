from django.contrib import admin
from ..admin_site import board_admin
from ..models import BoardMeetingVote
from ..forms import MeetingVoteForm


class MeetingVoteAdmin(admin.ModelAdmin):
	form = MeetingVoteForm


board_admin.register(BoardMeetingVote, MeetingVoteAdmin)
