from django import forms
from ..models import PersonalDeclaration


class PersonalDeclarationForm(forms.ModelForm):

    class Meta:
        model = PersonalDeclaration
        fields = '__all__'
