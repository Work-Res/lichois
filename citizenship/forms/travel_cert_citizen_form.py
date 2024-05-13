from django import forms
from ..models import TravelCertNonCitizen


class TravelCertNonCitizenForm(forms.ModelForm):

    class Meta:
        model = TravelCertNonCitizen
        fields = '__all__'
