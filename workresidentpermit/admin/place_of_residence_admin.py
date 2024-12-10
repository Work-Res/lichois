from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..admin_site import workresidencepermit_admin
from ..forms.place_of_residence_form import PlaceOfResidenceForm
from ..models import PlaceOfResidence


@admin.register(PlaceOfResidence, site=workresidencepermit_admin)
class PlaceOfResidenceAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):
    form = PlaceOfResidenceForm

    list_display: Tuple[str, ...] = (
        'country',
        'place_of_residence',
    )
    search_fields: Tuple[str, ...] = ('country', 'place_of_residence')
