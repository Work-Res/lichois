from django import forms
from ..models import WitnessDetails


class WitnessDetailsForm(forms.ModelForm):

    class Meta:
        model = WitnessDetails
        fields = '__all__'
