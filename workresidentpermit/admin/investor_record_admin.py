from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..admin_site import workresidencepermit_admin
from ..forms.investor_record_form import InvestorRecordForm
from ..models import InvestorRecord


@admin.register(InvestorRecord, site=workresidencepermit_admin)
class InvestorRecordAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):

    form = InvestorRecordForm

    list_display: Tuple[str, ...] = (
        'document_number',
        'company_name',
        'investor_address',
        'services_offered',
        'total_asset_value',)

    search_fields: Tuple[str, ...] = ('document_number', 'company_name',)

    fieldsets = (
        ("Investor Details", {
            "fields": (
                'company_name',
                'investor_address',
                'services_offered',
                'total_asset_value',
                'draw_salary',
                'reason_draw_salary',
                'citizen_employees',
                'non_citizen_employees',
                'shares_applicant',
                'shares_botswana_partners',
                'names_botswana_partners',
                'non_directors',
                'tax_registration_tin',
                'cipa_number',
                'applicant_qualifications',
                'bank_balance_value',
                'languages_competent',
                'language_other_specify',
                'residence_years',
                'investor_permit_period'
            ),
        }),
        audit_fieldset_tuple
    )

    radio_fields = {"draw_salary": admin.HORIZONTAL, }
