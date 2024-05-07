from django import forms
from ..models import Under20Citizenship


class Under20CitizenshipForm(forms.ModelForm):

    class Meta:
        model = Under20Citizenship
        fields = '__all__'
