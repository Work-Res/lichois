from django import forms
from ..models import DeclarationNaturalisationByForeignSpouse


class DeclNaturalisationByForeignSpouseForm(forms.ModelForm):

    class Meta:
        model = DeclarationNaturalisationByForeignSpouse
        fields = '__all__'
