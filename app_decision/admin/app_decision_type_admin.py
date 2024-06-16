from django.contrib import admin
from ..models import ApplicationDecisionType


class ApplicationDecisionTypeAdmin(admin.ModelAdmin):
	list_display = ('code', 'name')
	search_fields = ('code', 'name')
	list_filter = ('code', 'name')


admin.site.register(ApplicationDecisionType, ApplicationDecisionTypeAdmin)
