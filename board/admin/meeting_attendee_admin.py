from django.contrib import admin
from ..admin_site import board_admin
from ..models import MeetingAttendee
from ..forms import MeetingAttendeeForm


@admin.register(MeetingAttendee, site=board_admin)
class MeetingAttendeeAdmin(admin.ModelAdmin):

    form = MeetingAttendeeForm
