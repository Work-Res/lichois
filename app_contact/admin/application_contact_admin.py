from django.contrib import admin

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..models import ApplicationContact
from ..admin_site import contact_admin


@admin.register(ApplicationContact, site=contact_admin)
class ApplicationContactAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display = ['creator', 'modifier', 'country_code', 'contact_value', 'email', 'cell']
    search_fields = ['creator', 'modifier', 'contact_value']
