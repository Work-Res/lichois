"""
Django Admin
"""
from django.contrib import admin

from ..models import *

admin.site.register(EmergencyPermit)
admin.site.register(ExemptionCertificate)
admin.site.register(PermitAppeal)
admin.site.register(PermitCancellation)
admin.site.register(ResidencePermit)
admin.site.register(WorkPermit)
admin.site.register(Declaration)
admin.site.register(PlaceOfResidence)
admin.site.register(SpousePlaceOfResidence)
admin.site.register(EmploymentRecord)
admin.site.register(PermitReplacement)
admin.site.register(Dependant)
admin.site.register(VariationPermit)
