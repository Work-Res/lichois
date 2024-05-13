from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import TravelCertNonCitizen
from ..forms import TravelCertNonCitizenForm


@admin.register(TravelCertNonCitizen, site=citizenship_admin)
class TravelCertNonCitizenAdmin(admin.ModelAdmin):

    form = TravelCertNonCitizenForm
