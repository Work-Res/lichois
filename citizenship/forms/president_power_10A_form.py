from django import forms
from ..models import PresidentPower10A


class PresidentPower10AForm(forms.ModelForm):
    # TODO: Implement fields

    class Meta:
        model = PresidentPower10A
        fields = '__all__'
