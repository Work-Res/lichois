from django.contrib import admin
from ..admin_site import board_admin
from ..models import Region
from ..forms import RegionForm


class RegionAdmin(admin.ModelAdmin):
	form = RegionForm


board_admin.register(Region, RegionAdmin)
