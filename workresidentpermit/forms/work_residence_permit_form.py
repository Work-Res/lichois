from ..models import ResidencePermit
from django import forms

class ResidencePermitForm(forms.ModelForm):
    class Meta:
        model = ResidencePermit
        fields = '__all__'