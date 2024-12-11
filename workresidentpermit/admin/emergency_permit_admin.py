from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..admin_site import workresidencepermit_admin
from ..forms.emergency_permit_form import EmergencyPermitForm
from ..models import EmergencyPermit


@admin.register(EmergencyPermit, site=workresidencepermit_admin)
class EmergencyPermitAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):

     fieldsets = (
        ("Emergency Details", {
            "fields": ("nature_emergency","job_requirements", "emergency_period",'services_provided',),
           
        }),
        
        ("Do you have the Chief Immigration Officer's Authority/Waiver to await the outcome of your application for a resisdents permit in Botswana?", {
            "fields": ("chief_authorization",'capacity'),
        }),
    )
     search_fields: Tuple[str, ...] = ('nature_emergency', 'job_requirements', 'services_provided')
     Floolist_filter:Tuple[str, ...]= ('emergency_period',)

