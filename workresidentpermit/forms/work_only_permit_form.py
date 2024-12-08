from django import forms
from ..models import WorkPermit


class WorkPermitForm(forms.ModelForm):
    class Meta:
        model = WorkPermit
        fields = '__all__'