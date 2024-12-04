from django.contrib import admin

from ..models import SpousePlaceOfResidence

class SpousePlaceOfResidenceAdmin(admin.ModelAdmin):
    list_display = (
        'country',
        'place_of_residence',
    )
    search_fields = ('country', 'place_of_residence',)

admin.site.register(SpousePlaceOfResidence, SpousePlaceOfResidenceAdmin)