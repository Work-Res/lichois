from django.contrib import admin
from ..admin_site import decision_admin
from ..models import Region
from ..forms import RegionForm


@admin.register(Region, site=decision_admin)
class RegionAdmin(admin.ModelAdmin):

    form = RegionForm
