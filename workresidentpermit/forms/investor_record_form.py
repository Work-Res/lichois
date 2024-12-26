from django import forms
from ..models import InvestorRecord


class InvestorRecordForm(forms.ModelForm):

    class Meta:
        model = InvestorRecord
        fields = '__all__'
