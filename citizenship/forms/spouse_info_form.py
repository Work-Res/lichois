from django import forms
from ..models import SpouseInfo


class SpouseInfoForm(forms.ModelForm):

    class Meta:
        model = SpouseInfo
        fields = '__all__'
