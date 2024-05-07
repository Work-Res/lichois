from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import RenunciationOfCitizenship
from ..forms import RenunciationOfCitizenshipForm


@admin.register(RenunciationOfCitizenship, site=citizenship_admin)
class RenunciationOfCitizenshipAdmin(admin.ModelAdmin):

    form = RenunciationOfCitizenshipForm
