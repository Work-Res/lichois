from django import forms
from ..models import PlaceOfResidence


class PlaceOfResidenceForm(forms.ModelForm):

    class Meta:
        model = PlaceOfResidence
        fields = '__all__'
