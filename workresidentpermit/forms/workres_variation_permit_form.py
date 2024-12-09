from django import forms
from ..models import VariationPermit

class WorkResVariationPermitForm(forms.ModelForm):

    class Meta:
        model = VariationPermit
        fields = '__all__'