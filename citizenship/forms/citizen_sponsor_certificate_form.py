from django import forms
from ..models import CitizenSponsorCertificate


class CitizenSponsorCertificateForm(forms.ModelForm):

    class Meta:
        model = CitizenSponsorCertificate
        fields = '__all__'
