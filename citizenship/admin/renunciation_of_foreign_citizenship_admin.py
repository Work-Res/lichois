from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import RenunciationOfForeignCitizenship
from ..forms import RenunciationOfForeignCitizenshipForm


@admin.register(RenunciationOfForeignCitizenship, site=citizenship_admin)
class RenunciationOfForeignCitizenshipAdmin(admin.ModelAdmin):

    form = RenunciationOfForeignCitizenshipForm
