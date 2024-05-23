from django.contrib import admin

from ..admin_site import board_admin
from ..forms import MeetingInvitationForm
from ..models import MeetingInvitation


class MeetingInvitationAdmin(admin.ModelAdmin):
	list_display = ('id', 'board_meeting', 'invited_user', 'timestamp', 'status')
	search_fields = ('meeting', 'invited_user__username', 'status')
	list_filter = ('status',)
	form = MeetingInvitationForm


board_admin.register(MeetingInvitation, MeetingInvitationAdmin)
