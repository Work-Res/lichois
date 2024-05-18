from django import forms
from ..models import VotingProcess


class VotingProcessForm(forms.ModelForm):
	class Meta:
		model = VotingProcess
		fields = (
			'board',
			'has_started',
			'has_ended',
			'document_number',
		)
