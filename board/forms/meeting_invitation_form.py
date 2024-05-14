from django import forms
from ..models import MeetingInvitation


class MeetingInvitationForm(forms.ModelForm):
	class Meta:
		model = MeetingInvitation
		fields = '__all__'
