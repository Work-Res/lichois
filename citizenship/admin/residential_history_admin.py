from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import ResidentialHistory
from ..forms import ResidentialHistoryForm


@admin.register(ResidentialHistory, site=citizenship_admin)
class ResidentialHistoryAdmin(admin.ModelAdmin):

    form = ResidentialHistoryForm
