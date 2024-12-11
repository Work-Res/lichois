from django.contrib import admin
from typing import Tuple

from ..admin_site import travel_certificate_admin
from ..forms.travel_certificate_form import TravelCertificateForm
from ..models import TravelCertificate


@admin.register(TravelCertificate, site=travel_certificate_admin)
class TravelCertificateAdmin(admin.ModelAdmin):

    form = TravelCertificateForm

    list_display: Tuple[str, ...] = (
            'kraal_head_name',
            'chief_name',
            'clan_name',
            'date_issued',
            'mother_full_address',
        )

    search_fields: Tuple[str, ...] = (
            'kraal_head_name',
            'chief_name',
            'clan_name',
            'issuing_authority',
        )

