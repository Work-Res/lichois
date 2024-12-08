from django.contrib import admin
from typing import Tuple
from ..models import PlaceOfResidence

class PlaceOfResidenceAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = (
        'country',
        'place_of_residence',
    )
    search_fields: Tuple[str, ...] = ('country', 'place_of_residence')

admin.site.register(PlaceOfResidence, PlaceOfResidenceAdmin)