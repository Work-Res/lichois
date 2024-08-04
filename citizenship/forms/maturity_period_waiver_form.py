from django import forms
from ..models import MaturityPeriodWaiver


class MaturityPeriodWaiverForm(forms.ModelForm):
    # TODO: Implement fields

    class Meta:
        model = MaturityPeriodWaiver
        fields = '__all__'
