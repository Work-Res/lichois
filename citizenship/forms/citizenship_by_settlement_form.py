from django import forms
from ..models import CitizenshipBySettlement


class CitizenshipBySettlementForm(forms.ModelForm):

    class Meta:
        model = CitizenshipBySettlement
        fields = '__all__'
