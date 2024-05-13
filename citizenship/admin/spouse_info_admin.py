from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import SpouseInfo
from ..forms import SpouseInfoForm


@admin.register(SpouseInfo, site=citizenship_admin)
class SpouseInfoAdmin(admin.ModelAdmin):

    form = SpouseInfoForm
