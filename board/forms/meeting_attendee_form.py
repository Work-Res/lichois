from django import forms
from ..models import MeetingAttendee


class MeetingAttendeeForm(forms.ModelForm):

    class Meta:
        model = MeetingAttendee
        fields = '__all__'
