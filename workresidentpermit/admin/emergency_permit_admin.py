from django.contrib import admin
<<<<<<< Updated upstream

from ..models import EmergencyPermit

class EmergencyPermitAdmin(admin.ModelAdmin):
    list_display = (
        'nature_emergency',
        'job_requirements',
        'services_provided',
        'chief_authorization',
        'capacity',
        'emergency_period',
    )
    search_fields = ('nature_emergency', 'job_requirements', 'services_provided')
    list_filter = ('emergency_period',)

admin.site.register(EmergencyPermit, EmergencyPermitAdmin)
=======
from ..models import EmergencyPermit


class EmergencyPermitAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'permit_status', 'job_offer', 'qualification', 'years_of_study']
    search_fields = ['document_number']


admin.site.register(EmergencyPermit, EmergencyPermitAdmin)
>>>>>>> Stashed changes
