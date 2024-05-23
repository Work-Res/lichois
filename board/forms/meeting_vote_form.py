from django import forms
from ..models import BoardMeetingVote


class MeetingVoteForm(forms.ModelForm):
	class Meta:
		model = BoardMeetingVote
		fields = (
			'comments',
			'status',
			'document_number',
			'tie_breaker',
		)
