from django import forms
from ..models import KgosanaCertificate


class KgosanaCertificateForm(forms.ModelForm):

    class Meta:
        model = KgosanaCertificate
        fields = '__all__'
