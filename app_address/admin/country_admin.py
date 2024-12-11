from django.contrib import admin

from ..models import Country
from ..admin_site import address_admin


@admin.register(Country, site=address_admin)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code', 'iso_a2_code', 'iso_a3_code', 'cso_code', 'local', 'valid_from', 'valid_to']
    search_fields = ['name']
