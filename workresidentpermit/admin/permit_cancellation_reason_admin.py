from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import (
    BaseUrlModelAdminMixin, ModelAdminAuditFieldsMixin, audit_fieldset_tuple)

from ..models import PermitCancellationReason
from ..forms.cancellation_reason_form import WorkResPermitCancellationReasonForm
from ..admin_site import workresidencepermit_admin


@admin.register(PermitCancellationReason, site=workresidencepermit_admin)
class PermitCancellationReasonAdmin(ModelAdminAuditFieldsMixin, BaseUrlModelAdminMixin, admin.ModelAdmin):

	form = WorkResPermitCancellationReasonForm
	list_display: Tuple[str, ...] = ('reason_for_cancellation', 'other_reason', 'created', 'modified',)
	search_fields: Tuple[str, ...] = ('reason_for_cancellation',)

