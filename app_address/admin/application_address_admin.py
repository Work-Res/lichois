from django.contrib import admin

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..models import ApplicationAddress
from ..admin_site import address_admin


@admin.register(ApplicationAddress, site=address_admin)
class ApplicationAddressAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display = ['apartment_number', 'plot_number', 'country', 'city', 'district', 'village', 'ward', 'street_address', 'address_type', 'status', 'private_bag', 'po_box', 'person_type']
    search_fields = ['plot_number','private_bag', 'po_box']
