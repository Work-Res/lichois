from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import PersonalDeclaration
from ..forms import PersonalDeclarationForm


@admin.register(PersonalDeclaration, site=citizenship_admin)
class PersonalDeclarationAdmin(admin.ModelAdmin):

    form = PersonalDeclarationForm
