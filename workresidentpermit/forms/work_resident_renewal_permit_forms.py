from ..models import WorkPermit
from django import forms

class WorkResRenewalPermitForm(forms.ModelForm):
    class Meta:
        model = WorkPermit
        fields = '__all__'