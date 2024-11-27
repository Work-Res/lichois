from django.contrib import admin
from ..models import ApplicationAddress

class ApplicationAddressAdmin(admin.ModelAdmin):
    list_display = ['apartment_number', 'plot_number', 'country', 'city', 'district', 'village', 'ward', 'street_address', 'address_type', 'status', 'private_bag', 'po_box', 'person_type']
    search_fields = ['plot_number','private_bag', 'po_box']