from django import forms
from lichois.visa.models import BlueCardApplication


class BlueCardApplicationForm(forms.ModelForm):

    class Meta:
        model = BlueCardApplication
        fields = '__all__'
