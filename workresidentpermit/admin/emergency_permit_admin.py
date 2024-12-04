from django.contrib import admin

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