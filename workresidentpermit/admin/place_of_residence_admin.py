from django.contrib import admin
from typing import Tuple
from ..models import PlaceOfResidence
from ..forms.place_of_residence_form import PlaceOfResidenceForm
class PlaceOfResidenceAdmin(admin.ModelAdmin):
    form = PlaceOfResidenceForm

    list_display: Tuple[str, ...] = (
        'country',
        'place_of_residence',
    )
    search_fields: Tuple[str, ...] = ('country', 'place_of_residence')

admin.site.register(PlaceOfResidence, PlaceOfResidenceAdmin)