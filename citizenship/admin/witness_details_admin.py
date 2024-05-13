from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import WitnessDetails
from ..forms import WitnessDetailsForm


@admin.register(WitnessDetails, site=citizenship_admin)
class WitnessDetailsAdmin(admin.ModelAdmin):

    form = WitnessDetailsForm
