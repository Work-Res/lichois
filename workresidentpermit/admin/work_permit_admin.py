from django.contrib import admin
from ..models import WorkPermit
from typing import Tuple
from ..forms.work_only_permit_form import WorkPermitForm
class WorkPermitAdmin(admin.ModelAdmin):

    form = WorkPermitForm
    list_display: Tuple[str, ...]  = ('document_number', 'permit_status', 'job_offer', 'qualification', 'years_of_study')
    search_fields: Tuple[str, ...]  = ('document_number',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('document_number',)
        return self.readonly_fields

admin.site.register(WorkPermit, WorkPermitAdmin)