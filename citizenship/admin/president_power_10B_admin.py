from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import PresidentPower10B
from ..forms import PresidentPower10BForm


@admin.register(PresidentPower10B, site=citizenship_admin)
class PresidentPower10BAdmin(admin.ModelAdmin):
    # TODO: Implement fields

    form = PresidentPower10BForm
