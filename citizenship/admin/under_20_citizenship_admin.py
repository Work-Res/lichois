from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import Under20Citizenship
from ..forms import Under20CitizenshipForm


@admin.register(Under20Citizenship, site=citizenship_admin)
class Under20CitizenshipAdmin(admin.ModelAdmin):

    form = Under20CitizenshipForm
