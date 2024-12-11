from ..models import PermitReplacement
from django import forms


class WorkResReplacementPermitForm(forms.ModelForm):

    class Meta:
        model = PermitReplacement
        fields = ['date_issued', 'signature', 'date_signed']

        list_display = ['date_issued', 'signature', 'date_signed']


        fieldsets = ("Permit Replacement", {
            "fields": (
                "non_citizen_identifier", "document_number", "date_issued", 'signature', 'date_signed'
            )
        })
