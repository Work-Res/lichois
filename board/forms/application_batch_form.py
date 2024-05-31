from django import forms
from ..models import ApplicationBatch


class ApplicationBatchForm(forms.ModelForm):
    class Meta:
        model = ApplicationBatch
        fields = '__all__'

