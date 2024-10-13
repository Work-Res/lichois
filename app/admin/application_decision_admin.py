from django.contrib import admin
from ..models import ApplicationDecision, ApplicationDecisionType
from ..admin_site import app_admin


class ApplicationDecisionTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'process_types', 'valid_from', 'valid_to')
    search_fields = ('code', 'name', 'process_types')
    list_filter = ('valid_from', 'valid_to')

class ApplicationDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'final_decision_type', 'proposed_decision_type', 'created_at', 'updated_at')
    search_fields = ('final_decision_type__name', 'proposed_decision_type__name')
    list_filter = ('final_decision_type', 'proposed_decision_type', 'created_at', 'updated_at')
    raw_id_fields = ('final_decision_type', 'proposed_decision_type')
    
