from django.contrib import admin
from typing import Tuple
from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..models import Spouse
from ..admin_site import personal_details_admin


@admin.register(Spouse, site=personal_details_admin)
class SpouseAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display: Tuple[str, ...] = ('first_name', 'last_name', 'middle_name', 'maiden_name', 'country', 'place_birth', 'dob', 'is_applying_residence')
    search_fields: Tuple[str, ...] = ('first_name', 'last_name')

    fieldsets = (
        ("Spouse Details", {
            "fields": (
                'first_name', 'last_name',
                'middle_name', 'maiden_name',
                'country', 'place_birth', 'dob','is_applying_residence'
            ),
        }),

        audit_fieldset_tuple
    )
    radio_fields = {"is_applying_residence": admin.VERTICAL}