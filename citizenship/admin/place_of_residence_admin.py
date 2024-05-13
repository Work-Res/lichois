from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import PlaceOfResidence
from ..forms import PlaceOfResidenceForm


@admin.register(PlaceOfResidence, site=citizenship_admin)
class PlaceOfResidenceAdmin(admin.ModelAdmin):

    form = PlaceOfResidenceForm
