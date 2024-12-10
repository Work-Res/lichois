from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..admin_site import workresidencepermit_admin
from ..forms.emergency_permit_form import EmergencyPermitForm
from ..models import EmergencyPermit


@admin.register(EmergencyPermit, site=workresidencepermit_admin)
class EmergencyPermitAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):

    form = EmergencyPermitForm
    list_display: Tuple[str, ...] = (
        'nature_emergency',
        'job_requirements',
        'services_provided',
        'chief_authorization',
        'capacity',
        'emergency_period',
    )
    search_fields: Tuple[str, ...] = ('nature_emergency', 'job_requirements', 'services_provided')
    list_filter:Tuple[str, ...]= ('emergency_period',)

