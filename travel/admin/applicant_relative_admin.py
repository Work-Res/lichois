from django.contrib import admin

from typing import Tuple

from ..admin_site import travel_certificate_admin
from ..forms.applicant_relative_form import ApplicantRelativeForm
from ..models import ApplicantRelative


@admin.register(ApplicantRelative, site=travel_certificate_admin)
class ApplicationRelativeAdmin(admin.ModelAdmin):
    form = ApplicantRelativeForm
    list_display: Tuple[str, ...] = (
        'surname',
        'name',
        'relationship',
        'address',
    )
    search_fields: Tuple[str, ...] = (
        'surname',
        'name',
        'relationship',
    )
