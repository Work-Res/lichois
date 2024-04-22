from django import forms
from ..models import VisaApplication, VisaReferenceInline, DisposalMoneyInline
from ..models import ContactMethodInline


class VisaApplicationForm(forms.ModelForm):

    class Meta:
        model = VisaApplication
        fields = '__all__'


class VisaReferenceInlineForm(forms.ModelForm):

    class Meta:
        model = VisaReferenceInline
        fields = '__all__'


class DisposalMoneyInlineForm(forms.ModelForm):

    class Meta:
        model = DisposalMoneyInline
        fields = '__all__'


class ContactMethodInlineForm(forms.ModelForm):

    class Meta:
        model = ContactMethodInline
        fields = '__all__'
