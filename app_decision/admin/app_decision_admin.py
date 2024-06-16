from django.contrib import admin
from ..models import ApplicationDecision


class ApplicationDecisionAdmin(admin.ModelAdmin):
    pass


admin.register(ApplicationDecision, ApplicationDecisionAdmin)
