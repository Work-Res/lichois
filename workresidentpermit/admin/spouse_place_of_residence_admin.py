from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..admin_site import workresidencepermit_admin
from ..forms.spouse_place_of_residence_form import SpousePlaceOfResidenceForm
from ..models import SpousePlaceOfResidence


@admin.register(SpousePlaceOfResidence, site=workresidencepermit_admin)
class SpousePlaceOfResidenceAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):
    form = SpousePlaceOfResidenceForm

    list_display: Tuple[str, ...] = (
        'country',
        'place_of_residence',
    )
    search_fields: Tuple[str, ...] = ('country', 'place_of_residence',)
