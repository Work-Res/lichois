from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import NaturalisationOfForeignSpouse
from ..forms import NaturalisationOfForeignSpouseForm


@admin.register(NaturalisationOfForeignSpouse, site=citizenship_admin)
class NaturalisationOfForeignSpouseAdmin(admin.ModelAdmin):

    form = NaturalisationOfForeignSpouseForm
