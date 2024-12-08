from django import forms
from ..models import ExemptionCertificate


class ExemptionCertificateForm(forms.ModelForm):
    class Meta:
        model = ExemptionCertificate
        fields = '__all__'