from django import forms
from ..models import AdoptedChildRegistration


class AdoptedChildRegistrationForm(forms.ModelForm):

    class Meta:
        model = AdoptedChildRegistration
        fields = '__all__'
