from django import forms
from ..models import CertNaturalisationByForeignSpouse


class CertNaturalisationByForeignSpouseForm(forms.ModelForm):

    class Meta:
        model = CertNaturalisationByForeignSpouse
        fields = '__all__'
