from django import forms
from ..models import CitizenshipRenunciationDeclaration


class CitizenshipRenunciationDeclarationForm(forms.ModelForm):

    class Meta:
        model = CitizenshipRenunciationDeclaration
        fields = '__all__'
