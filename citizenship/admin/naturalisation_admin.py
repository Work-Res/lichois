from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import Naturalisation
from ..forms import NaturalisationForm


@admin.register(Naturalisation, site=citizenship_admin)
class NaturalisationAdmin(admin.ModelAdmin):

    form = NaturalisationForm
