from django import forms
from ..models import BoardMeeting


class BoardMeetingForm(forms.ModelForm):

    class Meta:
        model = BoardMeeting
        fields = '__all__'
