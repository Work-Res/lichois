from django import forms
from ..models import CitizenshipResumption


class CitizenshipResumptionForm(forms.ModelForm):

    class Meta:
        model = CitizenshipResumption
        fields = '__all__'
