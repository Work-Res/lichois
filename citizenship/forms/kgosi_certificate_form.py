from django import forms
from ..models import KgosiCertificate


class KgosiCertificateForm(forms.ModelForm):

    class Meta:
        model = KgosiCertificate
        fields = '__all__'
