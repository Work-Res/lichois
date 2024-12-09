from django import forms
from ..models import EmergencyPermit

class EmergencyPermitForm(forms.ModelForm):

    class Meta:
        model = EmergencyPermit
        fields = '__all__'