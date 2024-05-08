from django import forms
from ..models import LateCitizenshipRenunciation


class LateCitizenshipRenunciationForm(forms.ModelForm):

    class Meta:
        model = LateCitizenshipRenunciation
        fields = '__all__'
