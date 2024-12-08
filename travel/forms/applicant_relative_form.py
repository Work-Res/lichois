from django import forms
from ..models import ApplicantRelative


class ApplicantRelativeForm(forms.ModelForm):
    class Meta:
        model = ApplicantRelative
        fields = '__all__'