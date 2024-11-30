from django.contrib import admin

from ..models import ExemptionCertificate

class ExemptionCertificateAdmin(admin.ModelAdmin):
    list_display = (
        'business_name',
        'employment_capacity',
        'proposed_period',
    )
    search_fields = ('business_name', 'employment_capacity',)
    list_filter = ('proposed_period',)

admin.site.register(ExemptionCertificate, ExemptionCertificateAdmin)