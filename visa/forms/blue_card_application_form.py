from django import forms
from ..models import BlueCardApplication


class BlueCardApplicationForm(forms.ModelForm):

    class Meta:
        model = BlueCardApplication
        fields = '__all__'
