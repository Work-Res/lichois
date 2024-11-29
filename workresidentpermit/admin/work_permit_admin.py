from django.contrib import admin
from ..models import WorkPermit

class WorkPermitAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'permit_status', 'job_offer', 'qualification', 'years_of_study']
    search_fields = ['document_number']