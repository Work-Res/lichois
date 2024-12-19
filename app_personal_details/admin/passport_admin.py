from django.contrib import admin

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..models import Passport
from ..admin_site import personal_details_admin
from typing import Tuple

@admin.register(Passport, site=personal_details_admin)
class PassportAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    list_display: Tuple[str, ...] = ('passport_number', 'date_issued', 'place_issued', 'expiry_date', 'nationality', 'photo', 'previous_passport_number')
    search_fields: Tuple[str, ...] = ('passport_number',)

    list_filter: Tuple[str, ...] = ('passport_number', 'expiry_date')

    fieldsets = (
    ("Passport Information of Applicants", {
        "fields": (
            'passport_number', 'place_issued', 'date_issued', 'expiry_date',
        ),

    }),
     audit_fieldset_tuple

)
