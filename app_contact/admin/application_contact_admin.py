from django.contrib import admin
from ..models import ApplicationContact

class ApplicationContactAdmin(admin.ModelAdmin):
    list_display = ['creator', 'modifier', 'country_code', 'sub_type', 'contact_value', 'email', 'cell']
    search_fields = ['creator', 'modifier', 'contact_value']
    
admin.site.register(ApplicationContact, ApplicationContactAdmin)