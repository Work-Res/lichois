from django import forms
from ..models import ExemptionCertificateApplication


class ExemptionCertificateApplicationForm(forms.ModelForm):

    class Meta:
        model = ExemptionCertificateApplication
        fields = '__all__'
