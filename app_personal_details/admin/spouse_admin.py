from django.contrib import admin

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..models import Spouse
from ..admin_site import personal_details_admin


@admin.register(Spouse, site=personal_details_admin)
class SpouseAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'middle_name', 'maiden_name', 'country', 'place_birth', 'dob', 'passport']
    search_fields = ['first_name', 'last_name']
