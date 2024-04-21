from django.contrib import admin
from ..admin_site import decision_admin
from ..models import MeetingAttendee
from ..forms import MeetingAttendeeForm


@admin.register(MeetingAttendee, site=decision_admin)
class MeetingAttendeeAdmin(admin.ModelAdmin):

    form = MeetingAttendeeForm
