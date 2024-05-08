from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import CitizenshipBySettlement
from ..forms import CitizenshipBySettlementForm


@admin.register(CitizenshipBySettlement, site=citizenship_admin)
class CitizenshipBySettlementAdmin(admin.ModelAdmin):

    form = CitizenshipBySettlementForm
