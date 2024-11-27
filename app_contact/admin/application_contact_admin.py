from django.contrib import admin
from ..models import ApplicationContact

class ApplicationContactAdmin(admin.ModelAdmin):
    list_display = ['creator', 'modifier', 'country_code', 'country_type', 'sub_type', 'contact_value', 'preferred_method_com', 'email', 'cell']
    search_fields = ['creator', 'modifier', 'contact_value']