from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import DeclarationNaturalisationByForeignSpouse
from ..forms import DeclNaturalisationByForeignSpouseForm


@admin.register(DeclarationNaturalisationByForeignSpouse, site=citizenship_admin)
class DeclNaturalisationByForeignSpouseAdmin(admin.ModelAdmin):

    form = DeclNaturalisationByForeignSpouseForm
