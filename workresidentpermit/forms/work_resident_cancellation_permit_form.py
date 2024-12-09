from ..models import PermitCancellation
from django import forms

class WorkResCancellationPermitForm(forms.ModelForm):
    class Meta:
        model = PermitCancellation
        fields = '__all__'