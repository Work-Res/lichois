from django.contrib import admin
from ..models import Spouse


from ..admin_site import personal_details_admin


@admin.register(Spouse, site=personal_details_admin)
class SpouseAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'middle_name', 'maiden_name', 'country', 'place_birth', 'dob', 'passport']
    search_fields = ['first_name', 'last_name']
