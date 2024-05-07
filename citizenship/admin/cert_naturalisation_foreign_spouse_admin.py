from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import CertNaturalisationByForeignSpouse
from ..forms import CertNaturalisationByForeignSpouseForm


@admin.register(CertNaturalisationByForeignSpouse, site=citizenship_admin)
class CertNaturalisationByForeignSpouseAdmin(admin.ModelAdmin):

    form = CertNaturalisationByForeignSpouseForm
