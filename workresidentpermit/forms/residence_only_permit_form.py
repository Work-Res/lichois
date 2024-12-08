from django import forms
from ..models import ResidencePermit

class ResidencePermitForm(forms.ModelForm):
    class Meta:
        model = ResidencePermit
        fields = '__all__'