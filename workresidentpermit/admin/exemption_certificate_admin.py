from django.contrib import admin
from typing import Tuple

from ..models import ExemptionCertificate
from ..forms.exemption_certificate_form import ExemptionCertificateForm
from ..admin_site import workresidencepermit_admin 


@admin.register(ExemptionCertificate, site=workresidencepermit_admin)
class ExemptionCertificateAdmin(admin.ModelAdmin):

    form = ExemptionCertificateForm
    list_display: Tuple[str, ...] = (
        'business_name',
        'employment_capacity',
        'proposed_period',
    )
    search_fields: Tuple[str, ...]= ('business_name', 'employment_capacity',)
    list_filter: Tuple[str, ...]= ('proposed_period',)
