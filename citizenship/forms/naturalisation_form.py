from django import forms
from ..models import Naturalisation


class NaturalisationForm(forms.ModelForm):

    class Meta:
        model = Naturalisation
        fields = '__all__'