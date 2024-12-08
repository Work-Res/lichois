from django.contrib import admin
from typing import Tuple
from ..models import TravelCertificate
from ..forms.travel_certificate_form import TravelCertificate


class TravelCertificateAdmin(admin.ModelAdmin):

    form = TravelCertificate

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

admin.site.register(TravelCertificate, TravelCertificateAdmin)
