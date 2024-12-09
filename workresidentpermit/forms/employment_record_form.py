from django import forms
from ..models import EmploymentRecord

class EmploymentRecordForm(forms.ModelForm):
    class Meta:
        model = EmploymentRecord
        fields = '__all__'