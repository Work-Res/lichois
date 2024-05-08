from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import CitizenshipResumption
from ..forms import CitizenshipResumptionForm


@admin.register(CitizenshipResumption, site=citizenship_admin)
class CitizenshipResumptionAdmin(admin.ModelAdmin):

    form = CitizenshipResumptionForm
