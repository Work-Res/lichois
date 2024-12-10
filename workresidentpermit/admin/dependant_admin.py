from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..admin_site import workresidencepermit_admin
from ..forms.dependant_form import DependantForm
from ..models import Dependant


@admin.register(Dependant, site=workresidencepermit_admin)
class DependantAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):

    form = DependantForm
    list_display: Tuple[str, ...] = (
        'name',
        'age',
        'gender',
    )
    search_fields: Tuple[str, ...] = ('name', 'gender')
    list_filter: Tuple[str, ...] = ('gender', 'age')