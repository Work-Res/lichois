from django.contrib import admin
from ..models import ResidencePermit

class ResidencePermitAdmin(admin.ModelAdmin):
    list_display = ['document_number','language', 'permit_reason', 'previous_nationality', 'current_nationality', 'state_period_required', 'propose_work_employment', 'reason_applying_permit', 'documentary_proof', 'travelled_on_pass', 'is_spouse_applying_residence', 'ever_prohibited', 'sentenced_before', 'entry_place', 'arrival_date', 'preferred_method_comm', 'preferred_method_comm_value']
    search_fields = ['document_number']