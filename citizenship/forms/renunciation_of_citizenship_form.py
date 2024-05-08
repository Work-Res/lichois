from django import forms
from ..models import RenunciationOfCitizenship


class RenunciationOfCitizenshipForm(forms.ModelForm):

    class Meta:
        model = RenunciationOfCitizenship
        fields = '__all__'
