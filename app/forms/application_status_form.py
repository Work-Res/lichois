from django import forms
from ..models import ApplicationStatus


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'

