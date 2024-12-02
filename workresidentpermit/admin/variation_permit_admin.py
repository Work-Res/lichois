from django.contrib import admin

from ..models import VariationPermit

class VariationPermitAdmin(admin.ModelAdmin):
    list_display = (
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
    search_fields = (
        'existing_permit__document_number',
        'current_company_name',
        'new_company_name',
    )
    list_filter = (
        'has_separate_permises',
        'draw_salary',
        'person_type',
        'applicant_type',
    )

admin.site.register(VariationPermit, VariationPermitAdmin)