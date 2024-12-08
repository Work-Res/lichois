from django import forms
from ..models import Declaration

class DeclarationForm(forms.ModelForm):
    class Meta:
        model = Declaration
        fields = '__all__'