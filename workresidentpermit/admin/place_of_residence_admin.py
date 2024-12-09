from django.contrib import admin
from typing import Tuple

from ..admin_site import workresidencepermit_admin
from ..forms.place_of_residence_form import PlaceOfResidenceForm
from ..models import PlaceOfResidence


@admin.register(PlaceOfResidence, site=workresidencepermit_admin)
class PlaceOfResidenceAdmin(admin.ModelAdmin):
    form = PlaceOfResidenceForm

    list_display: Tuple[str, ...] = (
        'country',
        'place_of_residence',
    )
    search_fields: Tuple[str, ...] = ('country', 'place_of_residence')
