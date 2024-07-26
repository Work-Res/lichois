from django import forms
from ..models import VisaApplication, VisaReference


class VisaApplicationForm(forms.ModelForm):

    class Meta:
        model = VisaApplication
        fields = "__all__"


class VisaReferenceInlineForm(forms.ModelForm):

    class Meta:
        model = VisaReference
        fields = "__all__"
