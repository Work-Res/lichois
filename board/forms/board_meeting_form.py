from django import forms
from ..models import BoardMeeting


class BoardMeetingForm(forms.ModelForm):

    class Meta:
        model = BoardMeeting
        fields = (
            'title',
            'meeting_date',
            'meeting_start_time',
            'meeting_end_time',
            'description',
            'status',
            'minutes',
            'meeting_type',
            'location',
        )
