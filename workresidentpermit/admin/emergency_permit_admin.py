from django.contrib import admin

from ..models import EmergencyPermit
from typing import Tuple
from ..forms.emergency_permit_form import EmergencyPermitForm
class EmergencyPermitAdmin(admin.ModelAdmin):

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

admin.site.register(EmergencyPermit, EmergencyPermitAdmin)
