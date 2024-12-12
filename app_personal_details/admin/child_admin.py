from django.contrib import admin

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..models import Child
from ..admin_site import personal_details_admin
from typing import Tuple

@admin.register(Child, site=personal_details_admin)

class ChildAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dob', 'age', 'gender', 'is_applying_residence']
    search_fields: Tuple[str, ...] = ('first_name', 'last_name')

    fieldsets = (
    ("Particulars of children under the age of 18 years, by any marriage or adoption:", {
        "fields": (
            'last_name', 'first_name', 'dob', 'gender', 'is_applying_residence'
        ),
    }),
     audit_fieldset_tuple

)

    radio_fields = {"gender": admin.VERTICAL, "is_applying_residence": admin.VERTICAL}
