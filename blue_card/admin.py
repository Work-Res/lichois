from django.contrib import admin

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from .admin_site import blue_card_admin
from .models import BlueCard


@admin.register(BlueCard, site=blue_card_admin)
class BlueCardAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    """
    Admin interface for managing Person records in MLHA Services.
    """

    # Display options
    list_display = [
        'document_number', 'non_citizen_identifier'
    ]

    # Fieldsets for grouping fields in the admin form
    fieldsets = (
        ("Identifiers", {
            "fields": (
                'non_citizen_identifier', 'document_number',
            ),
        }),
        audit_fieldset_tuple
    )
