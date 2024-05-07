from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import CitizenshipRenunciationDeclaration
from ..forms import CitizenshipRenunciationDeclarationForm


@admin.register(CitizenshipRenunciationDeclaration, site=citizenship_admin)
class CitizenshipRenunciationDeclarationAdmin(admin.ModelAdmin):

    form = CitizenshipRenunciationDeclarationForm
