from django.contrib import admin

from typing import Tuple
from ..forms.applicant_relative_form import ApplicantRelativeForm
from ..models import ApplicantRelative

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

admin.site.register(ApplicantRelative, ApplicationRelativeAdmin)