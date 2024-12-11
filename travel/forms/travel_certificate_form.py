from django import forms
from ..models import TravelCertificate


class TravelCertificateForm(forms.ModelForm):
    class Meta:
        model = TravelCertificate
        fields = '__all__'