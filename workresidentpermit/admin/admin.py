"""
Django Admin
"""
from django.contrib import admin

from ..models import (
    EmergencyPermit,
    ExemptionCertificate,
    PermitAppeal,
    PermitCancellation,
    ResidencePermit,
    WorkPermit,
    Declaration,
    PlaceOfResidence,
    SpousePlaceOfResidence,
    EmploymentRecord,
    PermitReplacement,
    Dependant,
    VariationPermit,
)

"""
Django Admin
"""
from django.contrib import admin
from ..models import (
    EmergencyPermit,
    ExemptionCertificate,
    PermitAppeal,
    PermitCancellation,
    ResidencePermit,
    WorkPermit,
    Declaration,
    PlaceOfResidence,
    SpousePlaceOfResidence,
    EmploymentRecord,
    PermitReplacement,
    Dependant,
    VariationPermit,
)

class EmergencyPermitAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'nature_emergency', 'emergency_period']
    search_fields = ['document_number', 'nature_emergency']

class ExemptionCertificateAdmin(admin.ModelAdmin):
    list_display = ['document_number']
    search_fields = ['document_number']

class PermitAppealAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'appeal_type', 'appeal_date']
    search_fields = ['document_number']
    list_filter = ['appeal_type']

class PermitCancellationAdmin(admin.ModelAdmin):
    list_display = ['document_number']
    search_fields = ['document_number']

class ResidencePermitAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'language', 'arrival_date']
    search_fields = ['document_number']

class WorkPermitAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'permit_status', 'job_title', 'qualification']
    search_fields = ['document_number', 'job_title']
    list_filter = ['permit_status']

class DeclarationAdmin(admin.ModelAdmin):
    list_display = ['document_number']
    search_fields = ['document_number']

class PlaceOfResidenceAdmin(admin.ModelAdmin):
    list_display = ['document_number']
    search_fields = ['document_number']

class SpousePlaceOfResidenceAdmin(admin.ModelAdmin):
    list_display = ['document_number']
    search_fields = ['document_number']

class EmploymentRecordAdmin(admin.ModelAdmin):
    list_display = ['document_number']
    search_fields = ['document_number']

class PermitReplacementAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'certificate_status', 'date_signed']
    search_fields = ['document_number']
    list_filter = ['certificate_status']

class DependantAdmin(admin.ModelAdmin):
    list_display = ['document_number']
    search_fields = ['document_number']

class VariationPermitAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'current_company_name', 'new_company_name', 'expiry_date']
    search_fields = ['document_number', 'current_company_name', 'new_company_name']

admin.site.register(EmergencyPermit, EmergencyPermitAdmin)
admin.site.register(ExemptionCertificate, ExemptionCertificateAdmin)
admin.site.register(PermitAppeal, PermitAppealAdmin)
admin.site.register(PermitCancellation, PermitCancellationAdmin)
admin.site.register(ResidencePermit, ResidencePermitAdmin)
admin.site.register(WorkPermit, WorkPermitAdmin)
admin.site.register(Declaration, DeclarationAdmin)
admin.site.register(PlaceOfResidence, PlaceOfResidenceAdmin)
admin.site.register(SpousePlaceOfResidence, SpousePlaceOfResidenceAdmin)
admin.site.register(EmploymentRecord, EmploymentRecordAdmin)
admin.site.register(PermitReplacement, PermitReplacementAdmin)
admin.site.register(Dependant, DependantAdmin)
admin.site.register(VariationPermit, VariationPermitAdmin)