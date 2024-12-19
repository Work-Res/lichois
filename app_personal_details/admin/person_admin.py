from django.contrib import admin

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

# from base_module.model_mixins import (
#     NationalityModelMixin)
from ..admin_site import personal_details_admin
from ..models import Person
from typing import Tuple

@admin.register(Person, site=personal_details_admin)
class PersonAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    """
    Admin interface for managing Person records in MLHA Services.
    """

    # Display options
    list_display: Tuple[str, ...] = (
        'first_name', 'last_name', 'other_names', 'maiden_name',
        'marital_status', 'dob', 'gender', 'occupation',
        'qualification',
    )
    search_fields: Tuple[str, ...] = ('first_name', 'last_name')

    # Fieldsets for grouping fields in the admin form
    fieldsets = (
        ("Personal Details", {
            "fields": (
                'non_citizen_identifier', 'document_number',
                'last_name', 'first_name', 'other_names', 'maiden_name',
                'marital_status', 'dob', 'gender',
            ),
        }),
        ("Professional Details", {
            "fields": (
                'occupation', 'qualification',
            ),
        }),
        ("Nationality Details", {
            "fields": (
                'present_nationality', 'previous_nationality', 'country_birth', 'place_birth',
            ),
        }),
        audit_fieldset_tuple
    )

    radio_fields = {"gender": admin.VERTICAL, }
