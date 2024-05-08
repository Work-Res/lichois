from django.contrib import admin
from ..admin_site import board_admin
from ..models import InterestDeclaration
from ..forms import InterestDeclarationForm


@admin.register(InterestDeclaration, site=board_admin)
class InterestDeclarationAdmin(admin.ModelAdmin):

    form = InterestDeclarationForm
