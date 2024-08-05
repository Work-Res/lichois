from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import MaturityPeriodWaiver
from ..forms import MaturityPeriodWaiverForm


@admin.register(MaturityPeriodWaiver, site=citizenship_admin)
class MaturityWaiverPeriodAdmin(admin.ModelAdmin):
    # TODO: Implement fields

    form = MaturityPeriodWaiverForm
