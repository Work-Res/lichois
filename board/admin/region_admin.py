from django.contrib import admin

from ..admin_site import board_admin
from ..models import Region
from ..forms import RegionForm


@admin.register(Region, site=board_admin)
class RegionAdmin(admin.ModelAdmin):
	form = RegionForm

