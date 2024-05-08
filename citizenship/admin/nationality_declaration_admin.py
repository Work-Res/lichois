from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import NationalityDeclaration
from ..forms import NationalityDeclarationForm


@admin.register(NationalityDeclaration, site=citizenship_admin)
class NationalityDeclarationAdmin(admin.ModelAdmin):

    form = NationalityDeclarationForm
