from django.contrib import admin

from ..admin_site import board_admin
from ..forms import MeetingInvitationForm
from ..models import MeetingInvitation


@admin.register(MeetingInvitation, site=board_admin)
class MeetingInvitationAdmin(admin.ModelAdmin):
	list_display = ('id', 'board_meeting', 'invited_user', 'timestamp', 'status')
	search_fields = ('invited_user__username', 'status')
	list_filter = ('status',)
	form = MeetingInvitationForm

