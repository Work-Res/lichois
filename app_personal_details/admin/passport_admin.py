from django.contrib import admin

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..models import Passport
from ..admin_site import personal_details_admin


@admin.register(Passport, site=personal_details_admin)
class PassportAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display = ['passport_number', 'date_issued', 'place_issued', 'expiry_date', 'nationality', 'photo', 'previous_passport_number']
    search_fields = ['passport_number']
