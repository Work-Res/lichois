from django.contrib import admin

from ..models import PlaceOfResidence

class PlaceOfResidenceAdmin(admin.ModelAdmin):
    list_display = (
        'country',
        'place_of_residence',
    )
    search_fields = ('country', 'place_of_residence')

admin.site.register(PlaceOfResidence, PlaceOfResidenceAdmin)