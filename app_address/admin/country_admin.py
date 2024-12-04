from django.contrib import admin
from ..models import Country

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code', 'iso_a2_code', 'iso_a3_code', 'cso_code', 'local', 'valid_from', 'valid_to']
    search_fields = ['name']

admin.site.register(Country, CountryAdmin)