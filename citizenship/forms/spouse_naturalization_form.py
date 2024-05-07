from django import forms
from ..models import SpouseNaturalization


class SpouseNaturalizationForm(forms.ModelForm):

    class Meta:
        model = SpouseNaturalization
        fields = '__all__'
