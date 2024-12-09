from django.contrib import admin

from typing import Tuple

from ..admin_site import workresidencepermit_admin
from ..forms.workres_variation_permit_form import WorkResVariationPermitForm
from ..models import VariationPermit


@admin.register(VariationPermit, site=workresidencepermit_admin)
class VariationPermitAdmin(admin.ModelAdmin):

    form = WorkResVariationPermitForm

    list_display: Tuple[str,...] = (
        'existing_permit',
        'expiry_date',
        'current_company_name',
        'new_company_name',
        'new_company_location',
        'has_separate_permises',
        'draw_salary',
        'salary_per_annum',
        'new_company_employee_count',
        'financial_institution_name',
    )
    search_fields: Tuple[str,...] = (
        'existing_permit__document_number',
        'current_company_name',
        'new_company_name',
    )
    list_filter: Tuple[str,...] = (
        'has_separate_permises',
        'draw_salary',
        'person_type',
        'applicant_type',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('existing_permit',)
        return self.readonly_fields
