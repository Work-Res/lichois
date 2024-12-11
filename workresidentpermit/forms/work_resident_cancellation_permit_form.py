from ..models import PermitCancellation
from django import forms

class WorkResPermitCancellationForm(forms.ModelForm):
    class Meta:
        model = PermitCancellation
        fields = '__all__'