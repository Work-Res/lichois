from django.contrib import admin

from ..admin_site import visa_admin
from ..forms import VisaApplicationForm
from ..models import VisaApplication


@admin.register(VisaApplication, site=visa_admin)
class VisaApplicationAdmin(admin.ModelAdmin):

    form = VisaApplicationForm

    list_filter = ("visa_type", "no_of_entries")
    list_display = ("visa_type", "no_of_entries")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "visa_type",
                    "no_of_entries",
                    "bots_address",
                    "dom_address",
                    "durations_stay",
                    "travel_reasons",
                    "requested_valid_from",
                    "requested_valid_to",
                    "return_visa_to",
                    "return_valid_until",
                )
            },
        ),
        (
            "Audit Fields",
            {
                "fields": (
                    "created",
                    "modified",
                    "user_created",
                    "user_modified",
                    "hostname_created",
                    "hostname_modified",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    radio_fields = {
        "visa_type": admin.VERTICAL,
        "no_of_entries": admin.VERTICAL,
    }

    readonly_fields = (
        "created",
        "modified",
        "user_created",
        "user_modified",
        "hostname_created",
        "hostname_modified",
    )
