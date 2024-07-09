from django import forms
from ..models import VotingProcess


class VotingProcessForm(forms.ModelForm):
    class Meta:
        model = VotingProcess
        fields = (
            "board",
            "status",
            "batch",
            "board_meeting",
        )
