from django.contrib import admin
from ..admin_site import decision_admin
from ..models import BoardMeeting
from ..forms import BoardMeetingForm


@admin.register(BoardMeeting, site=decision_admin)
class BoardMeetingAdmin(admin.ModelAdmin):

    form = BoardMeetingForm
