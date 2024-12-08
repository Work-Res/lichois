from django.contrib import admin
from typing import Tuple
from ..models import SpousePlaceOfResidence

class SpousePlaceOfResidenceAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = (
        'country',
        'place_of_residence',
    )
    search_fields: Tuple[str, ...] = ('country', 'place_of_residence',)

admin.site.register(SpousePlaceOfResidence, SpousePlaceOfResidenceAdmin)