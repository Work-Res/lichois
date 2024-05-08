from django import forms
from ..models import RenunciationOfForeignCitizenship


class RenunciationOfForeignCitizenshipForm(forms.ModelForm):

    class Meta:
        model = RenunciationOfForeignCitizenship
        fields = '__all__'

