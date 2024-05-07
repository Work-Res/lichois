from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import OathOfAllegiance
from ..forms import OathOfAllegianceForm


@admin.register(OathOfAllegiance, site=citizenship_admin)
class OathOfAllegianceAdmin(admin.ModelAdmin):

    form = OathOfAllegianceForm
