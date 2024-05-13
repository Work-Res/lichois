from django import forms
from ..models import ResidentialHistory


class ResidentialHistoryForm(forms.ModelForm):

    class Meta:
        model = ResidentialHistory
        fields = '__all__'
