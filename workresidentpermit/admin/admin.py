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

from .res_permit_admin import *
from .work_permit_admin import *

admin.site.register(ResidencePermit, ResidencePermitAdmin)
admin.site.register(WorkPermit, WorkPermitAdmin)


# admin.site.register(EmergencyPermit, EmergencyPermitAdmin)
# admin.site.register(ExemptionCertificate, ExemptionCertificateAdmin)
# admin.site.register(PermitAppeal, PermitAppealAdmin)
# admin.site.register(PermitCancellation, PermitCancellationAdmin)
# admin.site.register(Declaration, DeclarationAdmin)
# admin.site.register(PlaceOfResidence, PlaceOfResidenceAdmin)
# admin.site.register(SpousePlaceOfResidence, SpousePlaceOfResidenceAdmin)
# admin.site.register(EmploymentRecord, EmploymentRecordAdmin)
# admin.site.register(PermitReplacement, PermitReplacementAdmin)
# admin.site.register(Dependant, DependantAdmin)
# admin.site.register(VariationPermit, VariationPermitAdmin)