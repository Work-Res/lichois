from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import PresidentPower10A
from ..forms import PresidentPower10AForm


@admin.register(PresidentPower10A, site=citizenship_admin)
class PresidentPower10AAdmin(admin.ModelAdmin):
    # TODO: Implement fields

    form = PresidentPower10AForm
