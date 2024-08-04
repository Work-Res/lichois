from django import forms
from ..models import PresidentPower10B


class PresidentPower10BForm(forms.ModelForm):
    # TODO: Implement fields

    class Meta:
        model = PresidentPower10B
        fields = '__all__'
