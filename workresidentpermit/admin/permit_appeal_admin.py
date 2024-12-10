from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..models import PermitAppeal
from ..forms.work_resident_permit_appeal_form import WorkResPermitAppealForm
from ..admin_site import workresidencepermit_admin


@admin.register(PermitAppeal, site=workresidencepermit_admin)
class PermitAppealAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):


    form = WorkResPermitAppealForm
    list_display: Tuple[str, ...] = (
        'reason_for_appeal',
        'appeal_type',
        'appeal_date',
    )
    search_fields: Tuple[str, ...] = ('reason_for_appeal', 'appeal_type')
    list_filter: Tuple[str, ...] = ('appeal_type', 'appeal_date')