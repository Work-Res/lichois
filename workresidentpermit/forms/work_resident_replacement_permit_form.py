from ..models import PermitReplacement
from django import forms

class WorkResReplacementPermitForm(forms.ModelForm):
    class Meta:
        model = PermitReplacement
        fields = '__all__'