from ..models import VariationPermit
from django import forms

class WorkResVariationPermitForm(forms.ModelForm):
    class Meta:
        model = VariationPermit
        fields = '__all__'