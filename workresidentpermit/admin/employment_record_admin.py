from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..admin_site import workresidencepermit_admin
from ..forms.employment_record_form import EmploymentRecordForm
from ..models import EmploymentRecord


@admin.register(EmploymentRecord, site=workresidencepermit_admin)
class EmploymentRecordAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):

    form = EmploymentRecordForm
    list_display: Tuple[str, ...] =  (
        'employer',
        'occupation',
        'duration',
        'names_of_trainees',
    )
    search_fields = ('employer', 'occupation', 'names_of_trainees',)
    list_filter = ('duration',)
