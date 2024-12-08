from django.contrib import admin
from typing import Tuple
from ..models import SpousePlaceOfResidence
from ..forms.spouse_place_of_residence_form import SpousePlaceOfResidenceForm
class SpousePlaceOfResidenceAdmin(admin.ModelAdmin):
    form = SpousePlaceOfResidenceForm

    list_display: Tuple[str, ...] = (
        'country',
        'place_of_residence',
    )
    search_fields: Tuple[str, ...] = ('country', 'place_of_residence',)

admin.site.register(SpousePlaceOfResidence, SpousePlaceOfResidenceAdmin)