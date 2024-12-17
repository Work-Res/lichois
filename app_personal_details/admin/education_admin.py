from django.contrib import admin

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..models import Education
from ..admin_site import personal_details_admin
from typing import Tuple

@admin.register(Education, site=personal_details_admin)
class EducationAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display: Tuple[str,...] = ('level', 'field_of_study', 'institution', 'start_date', 'end_date')
    search_fields: Tuple[str, ...] = ('field_of_study', 'institution')

    fieldsets = (
        ("Educational Details", {
            "fields": (
                'level', 'field_of_study',
                'institution',
            ),
        }),

        audit_fieldset_tuple
    )
