from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import LateCitizenshipRenunciation
from ..forms import LateCitizenshipRenunciationForm


@admin.register(LateCitizenshipRenunciation, site=citizenship_admin)
class LateCitizenshipRenunciationAdmin(admin.ModelAdmin):

    form = LateCitizenshipRenunciationForm
