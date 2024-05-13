from django import forms
from ..models import DCCertificate


class DCCertificateForm(forms.ModelForm):

    class Meta:
        model = DCCertificate
        fields = '__all__'
