from django.contrib import admin
from ..admin_site import decision_admin
from ..models import InterestDeclaration
from ..forms import InterestDeclarationForm


@admin.register(InterestDeclaration, site=decision_admin)
class InterestDeclarationAdmin(admin.ModelAdmin):

    form = InterestDeclarationForm
