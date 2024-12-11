from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..admin_site import workresidencepermit_admin
from ..forms.declaration_form import DeclarationForm
from ..models import Declaration


@admin.register(Declaration, site=workresidencepermit_admin)
class DeclarationAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):

    form = DeclarationForm
    list_display: Tuple[str, ...] = (
        'declaration_fname',
        'declaration_lname',
        'declaration_date',
        'signature',
    )
    search_fields: Tuple[str, ...] = ('declaration_fname', 'declaration_lname', 'signature',)
    list_filter: Tuple[str, ...] = ('declaration_date',)