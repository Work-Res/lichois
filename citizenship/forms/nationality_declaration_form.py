from django import forms
from ..models import NationalityDeclaration


class NationalityDeclarationForm(forms.ModelForm):

    class Meta:
        model = NationalityDeclaration
        fields = '__all__'

