from django import forms
from lichois.visa.models import ExemptionCertificateApplication


class ExemptionCertificateApplicationForm(forms.ModelForm):

    class Meta:
        model = ExemptionCertificateApplication
        fields = '__all__'
