from django import forms
from ..models import InterestDeclaration


class InterestDeclarationForm(forms.ModelForm):

    class Meta:
        model = InterestDeclaration
        fields = '__all__'
