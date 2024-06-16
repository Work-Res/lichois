from django.contrib import admin
from ..models import ApplicationDecisionType


class ApplicationDecisionTypeAdmin(admin.ModelAdmin):
	list_display = ('code', 'description', 'created_at', 'updated_at')
	search_fields = ('code', 'description')
	list_filter = ('code', 'description', 'created_at', 'updated_at')


admin.site.register(ApplicationDecisionType, ApplicationDecisionTypeAdmin)
