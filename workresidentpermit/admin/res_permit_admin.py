from django.contrib import admin
from typing import Tuple

from ..models import ResidencePermit
from ..forms.residence_only_permit_form import ResidencePermitForm
from ..admin_site import workresidencepermit_admin



@admin.register(ResidencePermit, site=workresidencepermit_admin)
class ResidencePermitAdmin(admin.ModelAdmin):
    form = ResidencePermitForm
    list_display: Tuple[str, ...] = (
        'document_number',
        'language',
        'permit_reason',
        'previous_nationality',
        'current_nationality',
        'state_period_required',
        'propose_work_employment',
        'reason_applying_permit',
        'documentary_proof',
        'travelled_on_pass',
        'is_spouse_applying_residence',
        'ever_prohibited',
        'sentenced_before',
        'entry_place',
        'arrival_date',
        'preferred_method_comm',
        'preferred_method_comm_value'
    )
    search_fields: Tuple[str, ...] = ('document_number',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('document_number',)
        return self.readonly_fields
