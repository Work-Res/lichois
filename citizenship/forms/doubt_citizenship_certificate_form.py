from django import forms
from ..models import DoubtCitizenshipCertificate


class DoubtCitizenshipCertificateForm(forms.ModelForm):
    # TODO: Implement fields

    class Meta:
        model = DoubtCitizenshipCertificate
        fields = '__all__'
