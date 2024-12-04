from django.contrib import admin

from ..models import EmploymentRecord

class EmploymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        'employer',
        'occupation',
        'duration',
        'names_of_trainees',
    )
    search_fields = ('employer', 'occupation', 'names_of_trainees',)
    list_filter = ('duration',)

admin.site.register(EmploymentRecord, EmploymentRecordAdmin)