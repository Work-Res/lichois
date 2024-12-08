from django import forms
from ..models import  Dependant


class DependantForm(forms.ModelForm):
    class Meta:
        model = Dependant
        fields = '__all__'