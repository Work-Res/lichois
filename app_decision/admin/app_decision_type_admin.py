from django.contrib import admin
from ..models import ApplicationDecisionType


class ApplicationDecisionTypeAdmin(admin.ModelAdmin):
	pass


admin.register(ApplicationDecisionType, ApplicationDecisionTypeAdmin)
