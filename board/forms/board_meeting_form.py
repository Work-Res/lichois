from django import forms
from ..models import BoardMeeting


class BoardMeetingForm(forms.ModelForm):

    class Meta:
        model = BoardMeeting
        fields = (
            'title',
            'meeting_date',
            'description',
            'status',
            'minutes',
            'meeting_type',
            'location',
        )
