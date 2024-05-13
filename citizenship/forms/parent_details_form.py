from django import forms
from ..models import ParentDetails


class ParentDetailsForm(forms.ModelForm):

    class Meta:
        model = ParentDetails
        fields = '__all__'
