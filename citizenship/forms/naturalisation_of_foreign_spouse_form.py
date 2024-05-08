from django import forms
from ..models import NaturalisationOfForeignSpouse



class NaturalisationOfForeignSpouseForm(forms.ModelForm):

    class Meta:
        model = NaturalisationOfForeignSpouse
        fields = '__all__'
