from django.contrib import admin
from ..admin_site import board_admin
from ..models import BoardMeeting
from ..forms import BoardMeetingForm


@admin.register(BoardMeeting, site=board_admin)
class BoardMeetingAdmin(admin.ModelAdmin):

    form = BoardMeetingForm
    search_fields = ["title", "meeting_date"]
