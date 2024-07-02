from django.contrib import admin
from ..models import ApplicationDecision


class ApplicationDecisionAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'final_decision_type')
    search_fields = ('document_number', 'final_decision_type')


admin.site.register(ApplicationDecision, ApplicationDecisionAdmin)