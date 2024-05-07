from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import SpouseNaturalization
from ..forms import SpouseNaturalizationForm


@admin.register(SpouseNaturalization, site=citizenship_admin)
class SpouseNaturalizationAdmin(admin.ModelAdmin):

    form = SpouseNaturalizationForm
