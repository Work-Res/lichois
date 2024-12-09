from django  import forms
from ..models import SpousePlaceOfResidence

class SpousePlaceOfResidenceForm(forms.ModelForm):
    class Meta:
        model = SpousePlaceOfResidence
        fields = '__all__'