from django import forms
from ..models import VariationPermit
from lichois_form_validators.form_validators import WorkResVariationPermitFormValidator
from lichois_form_validators import FormValidatorMixin

class WorkResVariationPermitForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = WorkResVariationPermitFormValidator

    class Meta:
        model = VariationPermit
        fields = '__all__'