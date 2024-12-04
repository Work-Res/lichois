from ..models import WorkPermit
from django import forms

class WorkResPermitForm(forms.ModelForm):
    class Meta:
        model = WorkPermit
        fields = '__all__'