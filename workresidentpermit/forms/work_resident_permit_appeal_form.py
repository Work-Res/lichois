from ..models import PermitAppeal
from django import forms

class WorkResPermitAppealForm(forms.ModelForm):
    class Meta:
        model = PermitAppeal
        fields = '__all__'