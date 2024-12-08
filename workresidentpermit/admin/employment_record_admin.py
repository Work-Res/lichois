from django.contrib import admin
from typing import Tuple
from ..models import EmploymentRecord
from ..forms.employment_record_form import EmploymentRecordForm
class EmploymentRecordAdmin(admin.ModelAdmin):

    form = EmploymentRecordForm
    list_display: Tuple[str, ...] =  (
        'employer',
        'occupation',
        'duration',
        'names_of_trainees',
    )
    search_fields = ('employer', 'occupation', 'names_of_trainees',)
    list_filter = ('duration',)

admin.site.register(EmploymentRecord, EmploymentRecordAdmin)