from ..models import PermitCancellationReason
from django import forms

class WorkResPermitCancellationReasonForm(forms.ModelForm):
    class Meta:
        model = PermitCancellationReason
        fields = '__all__'