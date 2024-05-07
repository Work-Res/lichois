from django import forms
from ..models import OathOfAllegiance


class OathOfAllegianceForm(forms.ModelForm):

    class Meta:
        model = OathOfAllegiance
        fields = '__all__'
