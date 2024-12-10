from django.contrib import admin

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..models import ParentalDetails
from ..admin_site import personal_details_admin


@admin.register(ParentalDetails, site=personal_details_admin)
class ParentalDetailsAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display = ['father', 'mother', 'father_address', 'mother_address']
    search_fields = ['father', 'mother']
